<template>
  <div class="page-wrap">
    <!-- 状态栏 -->
    <div v-if="showStatusBar" class="status-bar">
      <div class="status-left">
        <div class="signal-icon"></div>
        <span>WiFi</span>
      </div>
      <div class="status-right">
        <span>{{ currentTime }}</span>
        <div class="battery-icon"></div>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="main-container">
      <div v-if="errorMsg" style="color:#c0392b;background:#fdecea;padding:8px 12px;border-radius:8px;margin-bottom:12px;">{{ errorMsg }}</div>
      <!-- 今日重点区域：后端内容摘要 -->
      <div class="focus-area">
        <h2 class="focus-title">今日重点</h2>
        <div class="focus-content" v-html="todaySummaryHTML || (loading.list ? '正在拉取后端数据…' : '暂无数据')"></div>
      </div>

      <!-- 推荐内容（按模块分区展示） -->
      <div class="course-section">
        <h3 class="section-title">数学模块推荐</h3>
        <div
          v-for="item in topMath"
          :key="'math-' + item.id"
          class="course-card"
          @click="tapCard(item)"
        >
          <div class="course-header">
            <div class="course-badge">MA</div>
            <h4 class="course-title">{{ item.title }}</h4>
          </div>
          <p class="course-info">
            模块：{{ item.module }}｜子类：{{ item.subcategory }}
          </p>
        </div>
        <div class="more-row"><button class="more-btn" @click.stop="goMore('math')">查看更多</button></div>
      </div>

      <div class="course-section">
        <h3 class="section-title">机器学习模块推荐</h3>
        <div
          v-for="item in topML"
          :key="'ml-' + item.id"
          class="course-card"
          @click="tapCard(item)"
        >
          <div class="course-header">
            <div class="course-badge">ML</div>
            <h4 class="course-title">{{ item.title }}</h4>
          </div>
          <p class="course-info">
            模块：{{ item.module }}｜子类：{{ item.subcategory }}
          </p>
        </div>
        <div class="more-row"><button class="more-btn" @click.stop="goMore('ml')">查看更多</button></div>
      </div>

      <!-- 搜索结果预览（/api/v1/search/） -->
      <div class="course-section" v-if="searchResults.length">
        <h3 class="section-title">搜索结果</h3>
        <div
          v-for="item in searchResults"
          :key="'s-' + item.id"
          class="course-card"
          @click="tapCard(item)"
        >
          <div class="course-header">
            <div class="course-badge">{{ badgeOf(item.module) }}</div>
            <h4 class="course-title">{{ item.title }}</h4>
          </div>
          <div class="course-info markdown" v-html="renderPreview(item.content_body)"></div>
        </div>
      </div>
    </div>

    <!-- 底部导航栏（已迁移至原生 tabBar） -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { api, type ContentItem } from '../../utils/api'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

// 移除硬编码底部导航
const currentTime = ref('')
const showStatusBar = ref(false) // 临时隐藏顶部状态栏（设为 true 可恢复显示）

// Markdown 渲染器与安全过滤
const md = new MarkdownIt({ html: false, linkify: true, breaks: true, typographer: true })
function sanitize(html: string) { try { return DOMPurify.sanitize(html) } catch { return html } }
function renderPreview(markdownText: string) {
  const html = md.render(markdownText || '')
  return sanitize(html)
}

// 分类推荐
const topMath = ref<ContentItem[]>([])
const topML = ref<ContentItem[]>([])

const searchResults = ref<ContentItem[]>([])
const todaySummary = ref('')
const todaySummaryHTML = ref('')
const loading = ref({ list: false, search: false })
const errorMsg = ref('')
// 新增：记录本次进入页面选中的“今日重点”项，防止后续重复随机
const chosenHighlight = ref<ContentItem | null>(null)

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function tapCard(item?: ContentItem) {
  if (!item) return
  location.href = `#/pages/content/detail?id=${item.id}`
}

function goMore(module: string) {
  try {
    // 使用本地存储传递到课程页的预选模块
    localStorage.setItem('course_preferred_module', module)
  } catch {}
  // 课程是 tabBar 页面，推荐使用 switchTab；H5 下也兼容 hash 跳转
  // @ts-ignore
  if (typeof uni !== 'undefined' && uni.switchTab) {
    // @ts-ignore
    uni.switchTab({ url: '/pages/course/index' })
  } else {
    location.href = '#/pages/course/index'
  }
}

function handleScroll() {
  // 取消随滚动的视差效果，固定位置
  const parallax = document.querySelector('.focus-area') as HTMLElement | null
  if (parallax) parallax.style.transform = 'none'
}

function badgeOf(module: string) {
  if (!module) return 'ML'
  const up = module.toUpperCase()
  if (up.startsWith('MAT') || up === 'MATH') return 'MA'
  if (up.startsWith('DL')) return 'DL'
  return up.slice(0, 2)
}

function shortText(text: string, n = 80) {
  if (!text) return ''
  const t = text.replace(/\n+/g, ' ')
  return t.length > n ? t.slice(0, n) + '…' : t
}
// 新增：占位文案检测，过滤“开发中/敬请期待/暂无内容”等
function isPlaceholderBody(text: string) {
  const t = (text || '').trim()
  if (!t) return true
  const patterns = [
    /开发中/,
    /敬请期待/,
    /暂无(内容|数据)?/,
    /(完善|建设)中/,
    /under development/i,
    /coming soon/i,
  ]
  return patterns.some((p) => p.test(t))
}

async function fetchTopContents() {
  try {
    loading.value.list = true
    const [mathList, mlList] = await Promise.all([
      api.listContents({ module: 'math', limit: 5 }),
      api.listContents({ module: 'ml', limit: 5 }),
    ])
    topMath.value = mathList
    topML.value = mlList
    // 仅在本次进入页面第一次拉取时随机一次，且只选有真实正文的数据
    if (!chosenHighlight.value) {
      const pool = [...mathList, ...mlList].filter(
        (it) => it && it.content_body && !isPlaceholderBody(it.content_body)
      )
      if (pool.length) {
        const chosen = pool[Math.floor(Math.random() * pool.length)]
        chosenHighlight.value = chosen
        const body = chosen.content_body || ''
        todaySummary.value = shortText(body, 120)
        todaySummaryHTML.value = sanitize(md.render(body))
      } else {
        // 无可用内容则保持为空，模板会显示“暂无数据”
        chosenHighlight.value = null
        todaySummary.value = ''
        todaySummaryHTML.value = ''
      }
    }
  } catch (err: any) {
    console.error('fetchTopContents error:', err)
    errorMsg.value = err?.message || '拉取内容失败'
  } finally {
    loading.value.list = false
  }
}

async function fetchSearchSample() {
  try {
    loading.value.search = true
    const data = await api.search({ query: '回归', limit: 3 })
    searchResults.value = data.results || []
  } catch (err) {
    console.error('fetchSearchSample error:', err)
  } finally {
    loading.value.search = false
  }
}

let timer: number | undefined

onMounted(() => {
  updateTime()
  timer = window.setInterval(updateTime, 1000)
  // 取消滚动事件监听，避免“今日重点”随滚动位移
  // window.addEventListener('scroll', handleScroll, { passive: true })
  // 初始渲染时重置一次
  handleScroll()
  // 拉取后端数据（按模块）
  fetchTopContents()
  fetchSearchSample()
})

onBeforeUnmount(() => {
  if (timer) window.clearInterval(timer)
  // window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
* { margin: 0; padding: 0; box-sizing: border-box; }
.page-wrap { font-family: 'Times New Roman', serif; background: linear-gradient(135deg, #f8f6f0 0%, #f5f2e9 100%); min-height: 100vh; position: relative; }

/* 状态栏样式 */
.status-bar { background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: #d4af37; padding: 8px 16px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; font-weight: 500; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.status-left { display: flex; align-items: center; gap: 8px; }
.status-right { display: flex; align-items: center; gap: 8px; }
.signal-icon { background: linear-gradient(45deg, #d4af37, #f4d03f); width: 18px; height: 12px; position: relative; }
.signal-icon::before { content: ''; position: absolute; bottom: 0; left: 0; width: 3px; height: 4px; background: #d4af37; border-radius: 1px; }
.signal-icon::after { content: ''; position: absolute; bottom: 0; left: 4px; width: 3px; height: 6px; background: #d4af37; border-radius: 1px; }
.battery-icon { width: 24px; height: 12px; border: 1px solid #d4af37; border-radius: 2px; position: relative; background: linear-gradient(45deg, #d4af37, #f4d03f); }
.battery-icon::after { content: ''; position: absolute; right: -3px; top: 3px; width: 2px; height: 6px; background: #d4af37; border-radius: 1px; }

/* 主容器 */
.main-container { padding: 20px; padding-bottom: 80px; }

/* 今日重点区域 */
.focus-area { background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #2c3e50 100%); border-radius: 16px; padding: 24px; margin-bottom: 24px; position: sticky; top: 0; z-index: 1000; overflow: hidden; box-shadow: 0 8px 32px rgba(44, 62, 80, 0.3); }
.focus-area::before { content: ''; position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 70%); animation: float 6s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-20px) rotate(180deg); } }
.focus-title { color: #d4af37; font-size: 24px; font-weight: bold; margin-bottom: 12px; position: relative; z-index: 1; }
.focus-content { color: #ecf0f1; font-size: 16px; line-height: 1.6; position: relative; z-index: 1; }
/* 限制“今日重点”高度，显示 Markdown 片段并多行截断 */
.focus-content { display: -webkit-box; -webkit-line-clamp: 6; -webkit-box-orient: vertical; overflow: hidden; }
.focus-content :deep(h1), .focus-content :deep(h2), .focus-content :deep(h3) { margin: 6px 0; font-size: 1em; color: #f5f7fa; }
.focus-content :deep(code) { background: rgba(255,255,255,0.1); padding: 2px 4px; border-radius: 4px; }
.focus-content :deep(pre code) { display:block; background: rgba(0,0,0,0.25); padding: 8px; border-radius: 8px; overflow:auto; }

/* 课程卡片 */
.course-section { margin-bottom: 32px; }
.section-title { font-size: 20px; color: #2c3e50; margin-bottom: 16px; font-weight: bold; position: relative; }
.section-title::after { content: ''; position: absolute; bottom: -4px; left: 0; width: 60px; height: 2px; background: linear-gradient(90deg, #d4af37, #f4d03f); }
.course-card { background: rgba(255, 255, 255, 0.9); border-radius: 12px; padding: 20px; margin-bottom: 16px; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 1px solid rgba(212, 175, 55, 0.1); transition: all 0.3s ease; position: relative; overflow: hidden; }
.course-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #d4af37, #f4d03f); }
.course-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.course-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.course-badge { width: 32px; height: 32px; background: linear-gradient(135deg, #d4af37, #f4d03f); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #2c3e50; font-weight: bold; font-size: 14px; }
.course-title { font-size: 18px; color: #2c3e50; font-weight: bold; }
.course-info { color: #7f8c8d; font-size: 14px; line-height: 1.5; }
/* 搜索结果中的 Markdown 预览，做三行截断 */
.course-card .markdown { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.course-card .markdown :deep(h1), .course-card .markdown :deep(h2), .course-card .markdown :deep(h3) { margin: 4px 0; font-size: 1em; }
.course-card .markdown :deep(code) { background:#f6f6f6; padding: 2px 4px; border-radius: 4px; }

/* 底部导航栏 */
.nav-bar { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-top: 1px solid rgba(212, 175, 55, 0.2); padding: 12px 0; display: flex; justify-content: space-around; align-items: center; box-shadow: 0 -4px 16px rgba(0,0,0,0.1); }
.nav-item { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 8px 16px; border-radius: 8px; transition: all 0.3s ease; cursor: pointer; }
.nav-item.active { background: linear-gradient(135deg, #d4af37, #f4d03f); color: #2c3e50; }
.nav-text { font-size: 12px; }
.more-row { display: flex; justify-content: flex-end; margin-top: 4px; }
.more-btn { border: none; background: transparent; color: #d4af37; font-weight: 600; cursor: pointer; padding: 6px 8px; border-radius: 6px; }
.more-btn:hover { text-decoration: underline; }
</style>