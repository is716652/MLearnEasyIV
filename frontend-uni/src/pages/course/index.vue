<template>
  <div class="page-wrap">
    <div class="header">课程</div>
    <div class="grid">
      <button class="btn" :class="{active: current==='math'}" @click="goModule('math')">数学</button>
      <button class="btn" :class="{active: current==='ml'}" @click="goModule('ml')">机器学习</button>
      <button class="btn" :class="{active: current==='dl'}" @click="goModule('dl')">深度学习</button>
    </div>
    <div class="list">
      <div v-for="it in items" :key="it.id" class="item" @click="goDetail(it.id)">
        <div class="t">{{ it.title }}</div>
        <div class="s">{{ it.module }}｜{{ it.subcategory }}</div>
      </div>
      <div class="loadmore">
        <button v-if="!loading && hasMore" class="btn more" @click="loadMore">加载更多</button>
        <div v-else-if="loading" class="hint">正在加载…</div>
        <div v-else class="hint">已显示全部</div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type ContentItem } from '../../utils/api'

const items = ref<ContentItem[]>([])
const current = ref<'math'|'ml'|'dl'>('math')
const skip = ref(0)
const pageSize = 20
const loading = ref(false)
const hasMore = ref(true)

async function load(module: 'math'|'ml'|'dl', reset = true) {
  loading.value = true
  try {
    if (reset) {
      current.value = module
      skip.value = 0
      items.value = []
      hasMore.value = true
    }
    const data = await api.listContents({ module, skip: skip.value, limit: pageSize })
    if (reset) items.value = data
    else items.value = items.value.concat(data)
    skip.value += data.length
    hasMore.value = data.length === pageSize
  } finally {
    loading.value = false
  }
}

function goModule(m: 'math'|'ml'|'dl') { load(m, true) }
function goDetail(id: number) { location.href = `#/pages/content/detail?id=${id}` }
function loadMore() { if (!loading.value && hasMore.value) load(current.value, false) }

onMounted(() => {
  let initial: 'math'|'ml'|'dl' = 'math'
  try {
    const v = localStorage.getItem('course_preferred_module') || ''
    if (v === 'math' || v === 'ml' || v === 'dl') initial = v
    localStorage.removeItem('course_preferred_module')
  } catch {}
  load(initial, true)
})
</script>
<style scoped>
.page-wrap { padding: 16px; font-family: 'Times New Roman', serif; }
.header { font-size: 20px; font-weight: 700; color:#2c3e50; margin-bottom: 12px; }
.grid { display:flex; gap:8px; }
.btn { padding:8px 10px; border-radius: 8px; border: 1px solid #d4af37; background:#fff; cursor:pointer; }
.btn.active { background: linear-gradient(135deg, #d4af37, #f4d03f); color:#2c3e50; border-color: transparent; }
.list { margin-top: 12px; display:flex; flex-direction:column; gap:8px; }
.item { padding:12px; border:1px solid #eee; border-radius:8px; background:#fff; cursor:pointer; }
.t { font-weight:600; margin-bottom:6px; color:#2c3e50; }
.s { color:#7f8c8d; font-size: 14px; }
.loadmore { display:flex; justify-content:center; padding: 12px 0; }
.btn.more { min-width: 120px; }
.hint { color:#7f8c8d; }
</style>