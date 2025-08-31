<template>
  <div class="page-wrap">
    <div class="card">
      <div class="avatar">{{ isLogin ? (profile?.nickname || user?.username?.[0]?.toUpperCase() || '我') : 'ME' }}</div>
      <div class="info">
        <div class="name">{{ isLogin ? (profile?.nickname || user?.username) : '未登录用户' }}</div>
        <div class="sub">{{ isLogin ? (user?.email || '欢迎回来') : '欢迎使用「简单学机器学习」' }}</div>
      </div>
    </div>

    <div class="menu">
      <div class="menu-item" v-if="!isLogin" @click="goLogin">去登录</div>
      <div class="menu-item" v-else @click="goProfile">个人信息</div>
      <div class="menu-item" v-if="isLogin" @click="goFavorites">我的收藏</div>
      <div class="menu-item" v-if="isLogin" @click="onLogout">退出登录</div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../utils/api'

const isLogin = ref(false)
const user = ref<{ id: number; username: string; email: string } | null>(null)
const profile = ref<{ nickname?: string; avatar_url?: string; bio?: string } | null>(null)

function goLogin() { try { location.hash = '#/pages/auth/login' } catch {} }
function goProfile() { try { location.hash = '#/pages/user/profile' } catch {} }
function goFavorites() { try { location.hash = '#/pages/user/favorites' } catch {} }

async function refreshMe() {
  try {
    const me = await api.me()
    user.value = me
    const p = await api.getProfile().catch(() => null)
    profile.value = p
    isLogin.value = true
  } catch {
    isLogin.value = false
    user.value = null
    profile.value = null
  }
}

async function onLogout() {
  api.logout()
  await refreshMe()
  ;(uni as any)?.showToast?.({ title: '已退出', icon: 'success' })
}

// 初次进入页面时拉取一次
onMounted(() => { refreshMe() })
// 每次页面显示（从其他页面返回）时刷新登录状态
onShow(() => { refreshMe() })
</script>
<style scoped>
.page-wrap { padding: 16px; font-family: 'Times New Roman', serif; }
.card { display:flex; gap:12px; background:#fff; border-radius:12px; padding:12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); align-items:center; }
.avatar { width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg,#d4af37,#f4d03f); color:#2c3e50; display:flex; align-items:center; justify-content:center; font-weight:700; }
.info .name { font-weight:700; color:#2c3e50; }
.info .sub { color:#7f8c8d; font-size: 14px; }
.menu { margin-top: 12px; display:flex; flex-direction:column; gap:8px; }
.menu-item { background:#fff; padding:12px; border-radius:8px; border:1px solid #eee; cursor: pointer; }
</style>