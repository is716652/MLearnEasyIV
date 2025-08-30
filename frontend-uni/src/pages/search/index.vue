<template>
  <div class="page-wrap">
    <div class="header">
      <input v-model="q" class="search" placeholder="搜索算法、数学、代码…" @keyup.enter="doSearch" />
      <button class="btn" @click="doSearch">搜索</button>
    </div>
    <div class="result">
      <div v-if="loading">正在搜索…</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="!items.length">暂无结果</div>
      <div v-else>
        <div v-for="it in items" :key="it.id" class="item" @click="goDetail(it.id)">
          <div class="t">{{ it.title }}</div>
          <div class="s">{{ shortText(it.content_body) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { api, type ContentItem } from '../../utils/api'

const q = ref('回归')
const items = ref<ContentItem[]>([])
const loading = ref(false)
const error = ref('')

function shortText(t: string, n=100) {
  if (!t) return ''
  const s = t.replace(/\n+/g, ' ')
  return s.length > n ? s.slice(0, n) + '…' : s
}

async function doSearch() {
  error.value = ''
  loading.value = true
  try {
    const data = await api.search({ query: q.value, limit: 20 })
    items.value = data.results || []
  } catch (e: any) {
    error.value = e?.message || '搜索失败'
  } finally {
    loading.value = false
  }
}

function goDetail(id: number) {
  location.href = `#/pages/content/detail?id=${id}`
}

doSearch()
</script>
<style scoped>
.page-wrap { padding: 16px; font-family: 'Times New Roman', serif; }
.header { display:flex; gap:8px; }
.search { flex:1; padding:8px 10px; border:1px solid #ddd; border-radius:8px; }
.btn { padding: 8px 12px; border-radius:8px; border:1px solid #d4af37; background:#fff; cursor:pointer; }
.result { margin-top: 12px; display:flex; flex-direction:column; gap:8px; }
.item { padding:12px; border:1px solid #eee; border-radius:8px; background:#fff; cursor:pointer; }
.t { font-weight:600; margin-bottom:6px; color:#2c3e50; }
.s { color:#7f8c8d; font-size: 14px; }
</style>