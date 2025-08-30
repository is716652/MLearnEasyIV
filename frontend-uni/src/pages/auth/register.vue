<template>
  <view class="container">
    <text class="title">注册</text>
    <input class="input" type="text" placeholder="用户名" v-model="username" />
    <input class="input" type="password" placeholder="密码" v-model="password" />
    <button class="btn" @click="onRegister">注册</button>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const username = ref('')
const password = ref('')

function onRegister() {
  uni.showToast({ title: '模拟注册成功', icon: 'success' })
}
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.input { display:block; border:1px solid #ddd; padding:8px; margin:8px 0; }
.btn { background:#34c759; color:#fff; padding:10px; border:none; border-radius:4px; }
</style>