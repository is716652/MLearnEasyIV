<template>
  <view class="container">
    <text class="title">订单列表</text>
    <view class="order" v-for="i in 3" :key="i">订单 #{{ i }}</view>
  </view>
</template>

<script setup lang="ts">
</script>

<style scoped>
.container { padding: 16px; }
.title { font-size: 18px; font-weight: bold; margin-bottom: 12px; }
.order { background:#fff; border:1px solid #eee; padding:12px; border-radius:6px; margin-top:8px; }
</style>