<template>
  <view class="container">
    <text class="title">登录</text>
    <input class="input" type="text" placeholder="用户名" v-model="username" />
    <input class="input" type="password" placeholder="密码" v-model="password" />
    <button class="btn" @click="onLogin" :disabled="loading">{{ loading ? '登录中…' : '登录' }}</button>
    <view class="tip">没有账号？<text class="link" @click="goRegister">去注册</text></view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../utils/api'

const username = ref('')
const password = ref('')
const loading = ref(false)

function goRegister() {
  try { location.hash = '#/pages/auth/register' } catch { /* ignore */ }
}

async function onLogin() {
  if (!username.value || !password.value) {
    ;(uni as any)?.showToast?.({ title: '请输入用户名和密码', icon: 'none' })
    return
  }
  loading.value = true
  try {
    await api.login(username.value, password.value)
    ;(uni as any)?.showToast?.({ title: '登录成功', icon: 'success' })
    setTimeout(() => { try { location.hash = '#/pages/me/index' } catch {} }, 300)
  } catch (e: any) {
    console.error(e)
    ;(uni as any)?.showToast?.({ title: e?.message || '登录失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.input { display:block; border:1px solid #ddd; padding:8px; margin:8px 0; border-radius: 6px; }
.btn { background:#007aff; color:#fff; padding:10px; border:none; border-radius:6px; width:100%; }
.tip { margin-top: 10px; color:#666; font-size: 14px; }
.link { color:#007aff; margin-left:6px; }
</style>