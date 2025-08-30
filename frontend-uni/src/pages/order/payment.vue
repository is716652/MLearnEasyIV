<template>
  <view class="container">
    <text class="title">支付</text>
    <button class="btn" @click="onPay">模拟支付</button>
  </view>
</template>

<script setup lang="ts">
function onPay() {
  uni.showToast({ title: '模拟支付成功', icon: 'success' })
}
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.btn { background:#ff9500; color:#fff; padding:10px; border:none; border-radius:4px; }
</style>