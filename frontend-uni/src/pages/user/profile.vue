<template>
  <view class="container">
    <text class="title">个人中心</text>
    <view class="card" v-if="user">
      <view class="row"><text class="label">用户名：</text><text>{{ user.username }}</text></view>
      <view class="row"><text class="label">邮箱：</text><text>{{ user.email }}</text></view>
    </view>

    <view class="card">
      <view class="row"><text class="label">昵称</text><input class="input" v-model="form.nickname" placeholder="输入昵称" /></view>
      <view class="row"><text class="label">头像URL</text><input class="input" v-model="form.avatar_url" placeholder="https://..." /></view>
      <view class="row"><text class="label">简介</text><textarea class="textarea" v-model="form.bio" placeholder="一句话介绍自己" /></view>
      <button class="btn" @click="onSave" :disabled="saving">{{ saving ? '保存中…' : '保存' }}</button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../utils/api'

const user = ref<{ id: number; username: string; email: string } | null>(null)
const form = reactive<{ nickname?: string; avatar_url?: string; bio?: string }>({ nickname: '', avatar_url: '', bio: '' })
const saving = ref(false)

async function load() {
  try {
    user.value = await api.me()
  } catch {}
  try {
    const p = await api.getProfile()
    form.nickname = p?.nickname || ''
    form.avatar_url = p?.avatar_url || ''
    form.bio = p?.bio || ''
  } catch {}
}

async function onSave() {
  saving.value = true
  try {
    await api.updateProfile({ nickname: form.nickname, avatar_url: form.avatar_url, bio: form.bio })
    ;(uni as any)?.showToast?.({ title: '已保存', icon: 'success' })
  } catch (e: any) {
    console.error(e)
    ;(uni as any)?.showToast?.({ title: e?.message || '保存失败', icon: 'none' })
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.card { background:#fff; border:1px solid #eee; padding:12px; border-radius:6px; margin-bottom: 12px; }
.row { display:flex; align-items:center; gap:8px; margin: 8px 0; }
.label { width: 80px; color:#666; }
.input { flex: 1; border:1px solid #ddd; padding:8px; border-radius:6px; }
.textarea { width:100%; min-height: 72px; border:1px solid #ddd; padding:8px; border-radius:6px; resize: vertical; }
.btn { background:#007aff; color:#fff; padding:10px; border:none; border-radius:6px; width:100%; }
</style>