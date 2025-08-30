<template>
  <div class="page-wrap">
    <div class="header">
      <button class="back" @click="goBack">返回</button>
      <h2 class="title">{{ detail?.title || '加载中…' }}</h2>
    </div>

    <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

    <div class="container" v-if="detail">
      <section class="block">
        <h3>正文</h3>
        <div class="body" v-html="renderedBody"></div>
      </section>

      <section class="block" v-if="detail.formulas && Object.keys(detail.formulas).length">
        <h3>公式</h3>
        <div class="formula-list">
          <div v-for="(val, key) in detail.formulas" :key="key" class="formula-item">
            <div class="formula-key">{{ key }}</div>
            <div class="formula-tex" v-html="renderedFormulas[key] || toSafeText(val)"></div>
            <div v-if="formulaMeta[key]?.explanation" class="formula-explain">{{ formulaMeta[key]?.explanation }}</div>
            <div v-if="formulaMeta[key]?.symbols && Object.keys(formulaMeta[key].symbols).length" class="formula-symbols">
              <div class="symbols-title">符号表</div>
              <ul>
                <li v-for="(sv, sk) in formulaMeta[key].symbols" :key="sk"><span class="sym">{{ sk }}</span>：{{ sv }}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section class="block" v-if="detail.python_code">
        <h3>Python 代码</h3>
        <pre class="code"><code>{{ detail.python_code }}</code></pre>
      </section>

      <section class="block" v-if="detail.charts_data && Object.keys(detail.charts_data).length">
        <h3>图表</h3>
        <div class="charts">
          <div v-for="(val, key) in detail.charts_data" :key="key" class="chart-item">
            <div class="chart-title">{{ key }}</div>
            <template v-if="shouldRenderECharts(val)">
              <div class="chart-canvas" :ref="el => setChartEl(key, el)"></div>
            </template>
            <img v-else-if="isBase64Png(val)" :src="val" alt="chart" />
            <img v-else-if="isUrl(val)" :src="val" alt="chart" />
            <div v-else class="chart-raw">{{ toJSON(val) }}</div>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="loading">{{ loading ? '正在加载详情…' : '暂无数据' }}</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick, onBeforeUnmount } from 'vue'
import { api, type ContentItem } from '../../utils/api'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import * as echarts from 'echarts'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
  typographer: true
})

function sanitize(html: string) {
  try { return DOMPurify.sanitize(html) } catch { return html }
}

const detail = ref<ContentItem | null>(null)
const renderedBody = ref('')
const renderedFormulas = ref<Record<string, string>>({})
const formulaMeta = ref<Record<string, { explanation?: string; symbols?: Record<string,string> }>>({})
const errorMsg = ref('')
const loading = ref(true)

const chartEls = new Map<string, HTMLElement>()
const chartInstances = new Map<string, echarts.ECharts>()

function goBack() {
  history.length > 1 ? history.back() : (location.href = '#/pages/index/index')
}

function isBase64Png(v: any) {
  return typeof v === 'string' && /^data:image\/(png|jpeg);base64,/i.test(v)
}
function isUrl(v: any) {
  return typeof v === 'string' && /^(https?:)?\/\//i.test(v)
}
function toJSON(v: any) {
  try { return JSON.stringify(v) } catch { return String(v) }
}

function simpleEscapeHTML(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function toSafeText(v: any) {
  if (v == null) return ''
  if (typeof v === 'string') return v
  try { return simpleEscapeHTML(JSON.stringify(v)) } catch { return String(v) }
}

function renderFormulas() {
  renderedFormulas.value = {}
  formulaMeta.value = {}
  if (!detail.value?.formulas) return
  const result: Record<string, string> = {}
  const meta: Record<string, { explanation?: string; symbols?: Record<string,string> }> = {}
  for (const [key, raw] of Object.entries(detail.value.formulas)) {
    const obj = raw && typeof raw === 'object' ? raw as any : { latex: String(raw || '') }
    const latexText = obj.latex || ''
    meta[key] = { explanation: obj.explanation || '', symbols: (obj.symbols && typeof obj.symbols === 'object') ? obj.symbols : undefined }
    try {
      result[key] = katex.renderToString(String(latexText), { throwOnError: false, displayMode: true })
    } catch (e) {
      result[key] = `<code>${simpleEscapeHTML(String(latexText))}</code>`
    }
  }
  renderedFormulas.value = result
  formulaMeta.value = meta
}

function setChartEl(key: string, el: any) {
  if (el) chartEls.set(key, el as HTMLElement)
}

function shouldRenderECharts(val: any) {
  if (!val) return false
  if (typeof val === 'string') return false
  if (Array.isArray(val)) return true
  if (typeof val === 'object') {
    return !!(val.series || val.xAxis || val.yAxis || val.dataset)
  }
  return false
}

function buildOptionFromValue(val: any): echarts.EChartsOption {
  if (Array.isArray(val)) {
    return {
      tooltip: {},
      xAxis: { type: 'category', data: val.map((_: any, i: number) => i + 1) },
      yAxis: { type: 'value' },
      series: [{ type: 'line', data: val }]
    }
  }
  if (typeof val === 'object') return val as echarts.EChartsOption
  return { xAxis: {}, yAxis: {}, series: [] }
}

async function renderCharts() {
  if (!detail.value?.charts_data) return
  // dispose old
  for (const inst of chartInstances.values()) { inst.dispose() }
  chartInstances.clear()

  await nextTick()
  for (const [key, raw] of Object.entries(detail.value.charts_data)) {
    if (!shouldRenderECharts(raw)) continue
    const el = chartEls.get(key)
    if (!el) continue
    const inst = echarts.init(el)
    const option = buildOptionFromValue(raw)
    inst.setOption(option)
    chartInstances.set(key, inst)
  }
}

function getIdFromLocation(): number | null {
  // 1) 优先从 URL search 取（hash 之前）
  const url = new URL(location.href)
  let idStr = url.searchParams.get('id') || url.searchParams.get('content_id') || ''
  // 2) 再从 hash 片段中的查询参数取（#/pages/..?.=）
  if (!idStr) {
    const hash = location.hash || ''
    const qIndex = hash.indexOf('?')
    if (qIndex !== -1) {
      const qs = hash.slice(qIndex + 1)
      const sp = new URLSearchParams(qs)
      idStr = sp.get('id') || sp.get('content_id') || ''
    }
    // 3) 兼容路径型：#/pages/content/detail/123
    if (!idStr) {
      const m = hash.match(/content\/detail\/?(\d+)/)
      if (m && m[1]) idStr = m[1]
    }
  }
  // 4) 兜底：读取最近一次浏览的 id
  if (!idStr) {
    try {
      const last = localStorage.getItem('last_detail_id') || ''
      if (last) idStr = last
    } catch {}
  }
  const n = Number(idStr)
  return Number.isFinite(n) && n > 0 ? n : null
}

async function fetchDetailByCurrentId(force = false) {
  try {
    const id = getIdFromLocation()
    if (!id) {
      errorMsg.value = '参数缺失：id，正在返回上一页…'
      loading.value = false
      setTimeout(() => { goBack() }, 800)
      return
    }
    if (!force && detail.value?.id === id) return

    loading.value = true
    errorMsg.value = ''

    // 每次加载前清空/释放旧渲染
    renderedBody.value = ''
    renderedFormulas.value = {}
    formulaMeta.value = {}
    for (const inst of chartInstances.values()) { inst.dispose() }
    chartInstances.clear()

    const data = await api.getContentById(id)
    detail.value = data
    const raw = data.content_body || ''
    const html = md.render(raw)
    renderedBody.value = sanitize(html)
    try { localStorage.setItem('last_detail_id', String(id)) } catch {}

    renderFormulas()
    await renderCharts()
  } catch (e: any) {
    console.error(e)
    errorMsg.value = e?.message || '加载详情失败'
  } finally {
    loading.value = false
  }
}

function onRouteChanged() {
  fetchDetailByCurrentId()
}

onMounted(async () => {
  await fetchDetailByCurrentId(true)
  // 监听 hash 和浏览器历史变化，确保相同路径不同 id 时重新拉取
  window.addEventListener('hashchange', onRouteChanged)
  window.addEventListener('popstate', onRouteChanged)
})

onBeforeUnmount(() => {
  for (const inst of chartInstances.values()) { inst.dispose() }
  chartInstances.clear()
  window.removeEventListener('hashchange', onRouteChanged)
  window.removeEventListener('popstate', onRouteChanged)
})
</script>

<style scoped>
.page-wrap { padding: 16px; font-family: 'Times New Roman', serif; }
.header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.back { padding: 6px 12px; border: 1px solid #d4af37; background: #fff; border-radius: 6px; cursor: pointer; }
.title { font-size: 20px; color: #2c3e50; }
.container { display: flex; flex-direction: column; gap: 16px; }
.block { background: #fff; border-radius: 10px; padding: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); }
.body { color: #2c3e50; line-height: 1.7; /* 移除 white-space 以便 Markdown 自动换行 */ }
.body :deep(pre code) { display:block; background:#f9f9f9; padding:12px; border-radius:8px; overflow:auto; }
.body :deep(code) { background:#f6f6f6; padding:2px 4px; border-radius:4px; }
.body :deep(h1), .body :deep(h2), .body :deep(h3) { margin: 12px 0 8px; }
.body :deep(p) { margin: 8px 0; }
.formula-item { padding: 8px 0; border-bottom: 1px dashed #eee; }
.formula-key { font-weight: bold; color: #7f8c8d; margin-bottom: 4px; }
.formula-tex { margin: 6px 0; }
.formula-explain { color:#2c3e50; font-size:14px; margin-top:4px; }
.formula-symbols { margin-top:6px; }
.symbols-title { color:#95a5a6; font-size:12px; }
.formula-symbols ul { margin:4px 0 0 16px; padding:0; list-style: disc; color:#2c3e50; font-size:12px; }
.formula-symbols .sym { font-family: 'Latin Modern Math', 'Times New Roman', serif; }
.code { background: #f9f9f9; border-radius: 8px; padding: 12px; overflow: auto; }
.charts { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.chart-item { background: #fafafa; border: 1px solid #eee; border-radius: 8px; padding: 8px; }
.chart-title { font-size: 14px; color: #2c3e50; margin-bottom: 6px; }
.loading { text-align: center; color: #7f8c8d; margin-top: 40px; }
.error { color:#c0392b; background:#fdecea; padding:8px 12px; border-radius:8px; margin-bottom:12px; }
.chart-canvas { width: 100%; height: 260px; }
</style>