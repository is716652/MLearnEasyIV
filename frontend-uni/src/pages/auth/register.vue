<template>
  <view class="container">
    <text class="title">注册</text>
    <input class="input" type="text" placeholder="用户名" v-model="username" />
    <input class="input" type="text" placeholder="邮箱（可选）" v-model="email" />
    <input class="input" type="password" placeholder="密码" v-model="password" />
    <button class="btn" @click="onRegister" :disabled="loading">{{ loading ? '提交中…' : '注册' }}</button>
    <view class="tip">已有账号？<text class="link" @click="goLogin">去登录</text></view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api } from '../../utils/api'

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)

function goLogin() {
  try { location.hash = '#/pages/auth/login' } catch {}
}

async function onRegister() {
  if (!username.value || !password.value) {
    ;(uni as any)?.showToast?.({ title: '请输入用户名和密码', icon: 'none' })
    return
  }
  loading.value = true
  try {
    await api.register(username.value, email.value, password.value)
    ;(uni as any)?.showToast?.({ title: '注册成功，请登录', icon: 'success' })
    setTimeout(() => { goLogin() }, 300)
  } catch (e: any) {
    console.error(e)
    ;(uni as any)?.showToast?.({ title: e?.message || '注册失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.input { display:block; border:1px solid #ddd; padding:8px; margin:8px 0; border-radius: 6px; }
.btn { background:#34c759; color:#fff; padding:10px; border:none; border-radius:6px; width:100%; }
.tip { margin-top: 10px; color:#666; font-size: 14px; }
.link { color:#007aff; margin-left:6px; }
</style>