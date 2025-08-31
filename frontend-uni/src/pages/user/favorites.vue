<template>
  <view class="page">
    <view class="nav">
      <button class="back" @click="goBack">返回</button>
      <text class="title">我的收藏</text>
      <view style="width:56px"></view>
    </view>

    <!-- 工具栏：筛选、排序、管理、快捷导航 -->
    <view class="toolbar" v-if="loggedIn">
      <view class="row">
        <view class="chips">
          <view class="chip" :class="{active: selectedModule==='all'}" @click="setModule('all')">全部模块</view>
          <view class="chip" v-for="m in uniqueModules" :key="'m-'+m" :class="{active: selectedModule===m}" @click="setModule(m)">{{ m }}</view>
        </view>
        <view class="right">
          <button class="mini" :class="{primary: sortOrder==='newest'}" @click="setSort('newest')">最新</button>
          <button class="mini" :class="{primary: sortOrder==='oldest'}" @click="setSort('oldest')">最早</button>
          <button class="mini" @click="cycleGroupMode">分组：{{ groupModeLabel }}</button>
          <button class="mini warn" @click="toggleManage">{{ manageMode ? '完成' : '管理' }}</button>
        </view>
      </view>
      <view class="row" v-if="uniqueTags.length">
        <view class="chips scrollable">
          <view class="chip" :class="{active: selectedTag==='all'}" @click="setTag('all')">全部标签</view>
          <view class="chip" v-for="t in uniqueTags" :key="'t-'+t" :class="{active: selectedTag===t}" @click="setTag(t)">{{ t }}</view>
        </view>
      </view>
      <view class="row shortcuts">
        <button class="mini" @click="goHome">首页</button>
        <button class="mini" @click="goSearch">搜索</button>
        <button class="mini" @click="goCourse">课程</button>
      </view>
    </view>

    <!-- 未登录空态 -->
    <view v-if="!loggedIn" class="empty">
      <text>您尚未登录</text>
      <button class="btn" @click="goLogin">去登录</button>
    </view>

    <!-- 变化提示 -->
    <view v-if="changeMsg" class="hint">{{ changeMsg }}</view>

    <scroll-view v-else scroll-y class="list" @refresherrefresh="onPullDown" refresher-enabled>
      <view v-if="loading" class="loading">加载中...</view>
      <view v-else-if="visibleItems.length === 0" class="empty">
        <text>暂无收藏</text>
        <view class="guide">
          <text>去发现更多内容：</text>
          <button class="btn" @click="goSearch">去搜索</button>
          <button class="btn" @click="goCourse">看课程</button>
        </view>
      </view>
      <view v-else>
        <!-- 非分组视图 -->
        <template v-if="groupMode==='none'">
          <view v-for="fav in visibleItems" :key="fav.id" class="cell" :class="{ highlight: Number(fav.content_id)===changedId, selected: manageMode && selectedSet.has(Number(fav.content_id)) }" @click="cellClick(fav)">
            <view class="badge-container">
              <text v-if="isNewFavorite(fav)" class="badge badge-new">新增</text>
              <text v-if="isRecentlyUpdated(fav)" class="badge badge-upd">更新</text>
            </view>
            <view class="cell-main">
              <text class="cell-title">{{ fav.content?.title || '未找到内容' }}</text>
              <text class="cell-sub">{{ fav.content?.module || '-' }} / {{ fav.content?.subcategory || '-' }}</text>
              <text v-if="fav.note" class="cell-note">备注：{{ fav.note }}</text>
              <text class="cell-time">收藏于：{{ fmtTime(fav.created_at) }}</text>
              <view v-if="Array.isArray(normalizeTags(fav.content?.tags)) && normalizeTags(fav.content?.tags).length" class="tagline">
                <text class="tag" v-for="tg in normalizeTags(fav.content?.tags)" :key="tg">#{{ tg }}</text>
              </view>
            </view>
            <view class="cell-side">
              <label v-if="manageMode" class="checkbox">
                <input type="checkbox" :checked="selectedSet.has(Number(fav.content_id))" @change.stop="toggleSelect(Number(fav.content_id))" />
              </label>
              <button v-else class="del" @click.stop="remove(fav.content_id)">取消收藏</button>
            </view>
          </view>
        </template>
        <!-- 分组视图 -->
        <template v-else>
          <view v-for="sec in groupedVisible" :key="sec.key" class="group">
            <view class="group-header">{{ sec.title }}</view>
            <view v-for="fav in sec.items" :key="fav.id" class="cell" :class="{ highlight: Number(fav.content_id)===changedId, selected: manageMode && selectedSet.has(Number(fav.content_id)) }" @click="cellClick(fav)">
              <view class="badge-container">
                <text v-if="isNewFavorite(fav)" class="badge badge-new">新增</text>
                <text v-if="isRecentlyUpdated(fav)" class="badge badge-upd">更新</text>
              </view>
              <view class="cell-main">
                <text class="cell-title">{{ fav.content?.title || '未找到内容' }}</text>
                <text class="cell-sub">{{ fav.content?.module || '-' }} / {{ fav.content?.subcategory || '-' }}</text>
                <text v-if="fav.note" class="cell-note">备注：{{ fav.note }}</text>
                <text class="cell-time">收藏于：{{ fmtTime(fav.created_at) }}</text>
                <view v-if="Array.isArray(normalizeTags(fav.content?.tags)) && normalizeTags(fav.content?.tags).length" class="tagline">
                  <text class="tag" v-for="tg in normalizeTags(fav.content?.tags)" :key="tg">#{{ tg }}</text>
                </view>
              </view>
              <view class="cell-side">
                <label v-if="manageMode" class="checkbox">
                  <input type="checkbox" :checked="selectedSet.has(Number(fav.content_id))" @change.stop="toggleSelect(Number(fav.content_id))" />
                </label>
                <button v-else class="del" @click.stop="remove(fav.content_id)">取消收藏</button>
              </view>
            </view>
          </view>
        </template>
      </view>
    </scroll-view>

    <!-- 管理底栏 -->
    <view v-if="manageMode" class="manage-bar">
      <button class="mini" @click="selectAll">全选</button>
      <button class="mini" @click="clearSelection">清空</button>
      <button class="mini warn" @click="batchUnfavorite">批量取消收藏（{{ selectedSet.size }}）</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../utils/api'

const items = ref<any[]>([])
const loading = ref(false)
const loggedIn = ref(false)

// 偏好持久化
const PREFS_KEY = 'fav_prefs'
const selectedModule = ref<string>('all')
const selectedTag = ref<string>('all')
const sortOrder = ref<'newest'|'oldest'>('newest')
const groupMode = ref<'none'|'module'|'date'>('none')

function savePrefs() {
  try {
    const prefs = { selectedModule: selectedModule.value, selectedTag: selectedTag.value, sortOrder: sortOrder.value, groupMode: groupMode.value }
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs))
  } catch {}
}
function applyPrefs() {
  try {
    const raw = localStorage.getItem(PREFS_KEY)
    if (!raw) return
    const p = JSON.parse(raw || '{}')
    if (p && typeof p === 'object') {
      if (typeof p.selectedModule === 'string') selectedModule.value = p.selectedModule
      if (typeof p.selectedTag === 'string') selectedTag.value = p.selectedTag
      if (p.sortOrder === 'newest' || p.sortOrder === 'oldest') sortOrder.value = p.sortOrder
      if (p.groupMode === 'none' || p.groupMode === 'module' || p.groupMode === 'date') groupMode.value = p.groupMode
    }
  } catch {}
}
function ensureValidPrefs() {
  // 如果持久化的 module/tag 不在当前集合中，回退到 all
  if (selectedModule.value !== 'all' && !uniqueModules.value.includes(selectedModule.value)) selectedModule.value = 'all'
  if (selectedTag.value !== 'all' && !uniqueTags.value.includes(selectedTag.value)) selectedTag.value = 'all'
}

watch([selectedModule, selectedTag, sortOrder, groupMode], savePrefs)

const uniqueModules = computed(() => {
  const set = new Set<string>()
  for (const it of items.value) { if (it?.content?.module) set.add(String(it.content.module)) }
  return Array.from(set)
})
const uniqueTags = computed(() => {
  const set = new Set<string>()
  for (const it of items.value) {
    const arr = normalizeTags(it?.content?.tags)
    for (const t of arr) set.add(t)
  }
  return Array.from(set)
})

function setModule(m: string) { selectedModule.value = m }
function setTag(t: string) { selectedTag.value = t }
function setSort(s: 'newest'|'oldest') { sortOrder.value = s }

const groupModeLabel = computed(() => groupMode.value === 'none' ? '无' : (groupMode.value === 'module' ? '模块' : '日期'))
function cycleGroupMode() {
  groupMode.value = groupMode.value === 'none' ? 'module' : (groupMode.value === 'module' ? 'date' : 'none')
}

function normalizeTags(tags: any): string[] {
  if (!tags) return []
  if (Array.isArray(tags)) return tags.map(x => String(x))
  if (typeof tags === 'string') return tags.split(/[\,\s]+/).filter(Boolean)
  return []
}

function fmtTime(iso: string) { try { return new Date(iso).toLocaleString() } catch { return iso } }

const filteredItems = computed(() => items.value.filter((it) => {
  let ok = true
  if (selectedModule.value !== 'all') ok = ok && (it?.content?.module === selectedModule.value)
  if (selectedTag.value !== 'all') ok = ok && normalizeTags(it?.content?.tags).includes(selectedTag.value)
  return ok
}))

const visibleItems = computed(() => {
  const arr = [...filteredItems.value]
  arr.sort((a, b) => {
    const ta = new Date(a.created_at || 0).getTime()
    const tb = new Date(b.created_at || 0).getTime()
    return sortOrder.value === 'newest' ? (tb - ta) : (ta - tb)
  })
  return arr
})

// 分组后的可见数据
const groupedVisible = computed(() => {
  if (groupMode.value === 'none') return []
  const base = visibleItems.value
  if (groupMode.value === 'module') {
    const map = new Map<string, any[]>()
    for (const it of base) {
      const key = String(it?.content?.module || '-')
      if (!map.has(key)) map.set(key, [])
      map.get(key)!.push(it)
    }
    return Array.from(map.entries()).map(([k, v]) => ({ key: `m-${k}`, title: `模块：${k}`, items: v }))
  }
  // date 分组：按 YYYY-MM-DD
  const map = new Map<string, any[]>()
  for (const it of base) {
    const d = new Date(it.created_at || 0)
    const key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
    if (!map.has(key)) map.set(key, [])
    map.get(key)!.push(it)
  }
  // 日期组按时间降序排列
  const sections = Array.from(map.entries()).map(([k, v]) => ({ key: `d-${k}`, title: k, items: v }))
  sections.sort((a, b) => (a.title < b.title ? 1 : -1))
  return sections
})

// 管理模式
const manageMode = ref(false)
const selectedSet = ref<Set<number>>(new Set())
function toggleManage() { manageMode.value = !manageMode.value; selectedSet.value = new Set() }
function toggleSelect(id: number) {
  const s = new Set(selectedSet.value)
  if (s.has(id)) s.delete(id); else s.add(id)
  selectedSet.value = s
}
function selectAll() { selectedSet.value = new Set(visibleItems.value.map(x => Number(x.content_id))) }
function clearSelection() { selectedSet.value = new Set() }

async function batchUnfavorite() {
  const ids = Array.from(selectedSet.value)
  if (!ids.length) { (uni as any)?.showToast?.({ title: '请选择要取消的收藏', icon: 'none' }); return }
  try {
    await mapLimit(ids, 6, async (id) => { try { await api.removeFavorite(id) } catch {} })
    items.value = items.value.filter(x => !selectedSet.value.has(Number(x.content_id)))
    selectedSet.value = new Set()
    manageMode.value = false
    ;(uni as any)?.showToast?.({ title: '已批量取消', icon: 'success' })
  } catch (e:any) {
    console.error(e)
    ;(uni as any)?.showToast?.({ title: '部分操作失败', icon: 'none' })
  }
}

// 返回联动高亮
const changedId = ref<number | null>(null)
const changeMsg = ref('')
function applyChangeHighlight() {
  let obj: any = null
  try { const raw = sessionStorage.getItem('fav_change') || ''; obj = raw ? JSON.parse(raw) : null } catch {}
  if (!obj) return
  try { sessionStorage.removeItem('fav_change') } catch {}
  const id = Number(obj.id)
  if (obj.action === 'added') {
    changeMsg.value = '已从详情页收藏，已高亮显示'
    changedId.value = id
    setTimeout(() => { changedId.value = null; changeMsg.value = '' }, 2000)
  } else if (obj.action === 'removed') {
    // 同步移除并提示
    items.value = items.value.filter(x => Number(x.content_id) !== id)
    changeMsg.value = '已从详情页取消收藏'
    setTimeout(() => { changeMsg.value = '' }, 1800)
  }
}

function cellClick(fav: any) {
  if (manageMode.value) { toggleSelect(Number(fav.content_id)); return }
  openDetail(fav.content_id)
}

function goBack() {
  try { history.length > 1 ? history.back() : (location.hash = '#/pages/me/index') } catch { location.hash = '#/pages/me/index' }
}
function goLogin() { location.hash = '#/pages/auth/login' }
function goHome() { location.hash = '#/pages/index/index' }
function goSearch() { location.hash = '#/pages/search/index' }
function goCourse() { location.hash = '#/pages/course/index' }
function openDetail(id: number) { location.hash = `#/pages/content/detail?id=${id}` }

// 并发+缓存的回退构建
const contentCache = new Map<number, any>()
async function getContentSummaryCached(id: number) {
  if (contentCache.has(id)) return contentCache.get(id)
  const c = await api.getContentById(id)
  const summary = { id: c.id, title: c.title, module: (c as any).module, subcategory: (c as any).subcategory, tags: (c as any).tags, created_at: (c as any).created_at, updated_at: (c as any).updated_at }
  contentCache.set(id, summary)
  return summary
}

async function mapLimit<T, R>(arr: T[], limit: number, iterator: (item: T, index: number) => Promise<R>): Promise<R[]> {
  const ret: R[] = new Array(arr.length)
  let i = 0
  const workers = new Array(Math.min(limit, arr.length)).fill(0).map(async () => {
    while (true) {
      const idx = i++
      if (idx >= arr.length) break
      ret[idx] = await iterator(arr[idx], idx)
    }
  })
  await Promise.all(workers)
  return ret
}

async function buildFromRawFavorites() {
  try {
    const raws = await api.listFavorites()
    if (!Array.isArray(raws) || raws.length === 0) { items.value = []; return }
    const results = await mapLimit(raws, 6, async (f) => {
      try {
        const c = await getContentSummaryCached(Number(f.content_id))
        return { id: f.id, content_id: f.content_id, note: f.note, created_at: f.created_at, content: c }
      } catch {
        return { id: f.id, content_id: f.content_id, note: f.note, created_at: f.created_at, content: null }
      }
    })
    items.value = results
  } catch {
    items.value = []
  }
}

async function load() {
  loading.value = true
  try {
    await api.me()
    loggedIn.value = true
  } catch (e:any) {
    loggedIn.value = false
    items.value = []
    loading.value = false
    return
  }

  try {
    const list = await api.listFavoritesWithContent()
    if (Array.isArray(list) && list.length > 0) {
      items.value = list
    } else {
      await buildFromRawFavorites()
    }
  } catch (e:any) {
    await buildFromRawFavorites()
    ;(uni as any)?.showToast?.({ title: '获取收藏失败，已回退', icon: 'none' })
  } finally {
    loading.value = false
    ensureValidPrefs()
    applyChangeHighlight()
  }
}

async function onPullDown() {
  await load()
}

async function remove(content_id: number) {
  try {
    await api.removeFavorite(content_id)
    items.value = items.value.filter(x => Number(x.content_id) !== Number(content_id))
    if (items.value.length === 0) {
      ;(uni as any)?.showToast?.({ title: '已取消收藏', icon: 'success' })
    }
  } catch (e:any) {
    alert(e?.message || '操作失败')
  }
}

// 徽标逻辑
const NEW_MS = 1000 * 60 * 60 * 48 // 48 小时内为“新增”
const UPDATED_MS = 1000 * 60 * 60 * 72 // 72 小时内为“更新”
function isNewFavorite(fav: any) {
  try { return Date.now() - new Date(fav?.created_at || 0).getTime() <= NEW_MS } catch { return false }
}
function isRecentlyUpdated(fav: any) {
  try {
    const up = fav?.content?.updated_at
    if (!up) return false
    return Date.now() - new Date(up).getTime() <= UPDATED_MS
  } catch { return false }
}

applyPrefs()
onMounted(load)
onShow(() => { load() })
</script>

<style scoped>
.page { padding: 12px; }
.nav { display:flex; align-items:center; justify-content:space-between; padding: 8px 0; }
.back { padding: 6px 10px; border:1px solid #d4af37; background:#fff; border-radius:6px; }
.title { font-size: 18px; font-weight: 600; }
.toolbar { display:flex; flex-direction:column; gap:8px; margin-bottom:8px; }
.row { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.right { display:flex; gap:6px; }
.chips { display:flex; gap:6px; flex-wrap:wrap; }
.chips.scrollable { overflow-x:auto; white-space:nowrap; }
.chip { padding:4px 8px; border:1px solid #eee; border-radius:999px; font-size:12px; background:#fff; color:#555; cursor:pointer; }
.chip.active { background:#2c3e50; color:#fff; border-color:#2c3e50; }
.shortcuts { gap:8px; }
.actions { display:flex; gap:8px; margin-bottom:8px; }
.mini { font-size:12px; padding:4px 8px; border:1px solid #eee; background:#fff; border-radius:6px; }
.mini.primary { background:#2c3e50; color:#fff; border-color:#2c3e50; }
.mini.warn { color:#d33; border-color:#f0d0d0; }
.list { height: calc(100vh - 180px); }
.cell { position: relative; display:flex; align-items:flex-start; justify-content:space-between; gap:8px; padding:12px; background:#fff; border-radius:8px; margin-bottom:10px; box-shadow:0 1px 2px rgba(0,0,0,0.04); transition: background-color .3s ease; }
.cell.highlight { animation: glow 1.2s ease-in-out 1; background:#fffbe6; }
@keyframes glow { 0% { background:#fff; } 30% { background:#fffbe6; } 100% { background:#fff; } }
.cell.selected { outline: 2px solid #2c3e50; }
.cell-main { display:flex; flex-direction:column; gap:4px; }
.cell-title { font-size:16px; font-weight:600; }
.cell-sub { font-size:12px; color:#888; }
.cell-note { font-size:12px; color:#666; }
.cell-time { font-size:12px; color:#999; }
.tagline { display:flex; flex-wrap:wrap; gap:6px; margin-top:4px; }
.tag { font-size:12px; color:#2c3e50; background:#f2f2f2; padding:2px 6px; border-radius:999px; }
.cell-side { display:flex; align-items:center; gap:8px; }
.del { background:#f5f5f5; color:#d33; border:1px solid #f0d0d0; border-radius:6px; padding: 6px 10px; }
.empty { padding: 24px; text-align:center; color:#666; }
.loading { padding: 24px; text-align:center; color:#888; }
.btn { margin-top: 8px; padding:8px 12px; border:1px solid #d4af37; background:#fff; border-radius:6px; }
.hint { margin: 6px 0; color:#2c3e50; background:#f5f9ff; border:1px solid #d0e3ff; padding:6px 10px; border-radius:6px; }
.manage-bar { position: fixed; left: 0; right: 0; bottom: 0; display:flex; gap:8px; justify-content: center; padding: 10px; background: rgba(255,255,255,0.96); box-shadow: 0 -2px 8px rgba(0,0,0,0.06); }
.checkbox { width: 20px; height: 20px; border:1px solid #ccc; border-radius:4px; display:flex; align-items:center; justify-content:center; }
.guide { margin-top: 12px; display:flex; flex-direction:column; gap:8px; align-items:center; }

/* 分组 */
.group { margin-bottom: 14px; }
.group-header { position: sticky; top: 0; background: #fafafa; color:#555; padding: 6px 8px; border-left: 3px solid #2c3e50; border-radius: 4px; margin-bottom: 8px; z-index: 1; }

/* 徽标 */
.badge-container { position:absolute; top:6px; right:10px; display:flex; gap:6px; }
.badge { font-size:10px; padding:2px 6px; border-radius:999px; color:#fff; }
.badge-new { background:#28a745; }
.badge-upd { background:#ff9800; }
</style>