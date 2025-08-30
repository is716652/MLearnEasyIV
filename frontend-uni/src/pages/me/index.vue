<template>
  <div class="page-wrap">
    <div class="card">
      <div class="avatar">ME</div>
      <div class="info">
        <div class="name">未登录用户</div>
        <div class="sub">欢迎使用「简单学机器学习」</div>
      </div>
    </div>

    <div class="menu">
      <div class="menu-item">个人信息</div>
      <div class="menu-item">订单记录</div>
      <div class="menu-item">设置</div>
    </div>
  </div>
</template>
<script setup lang="ts">
</script>
<style scoped>
.page-wrap { padding: 16px; font-family: 'Times New Roman', serif; }
.card { display:flex; gap:12px; background:#fff; border-radius:12px; padding:12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); align-items:center; }
.avatar { width:48px; height:48px; border-radius:50%; background:linear-gradient(135deg,#d4af37,#f4d03f); color:#2c3e50; display:flex; align-items:center; justify-content:center; font-weight:700; }
.info .name { font-weight:700; color:#2c3e50; }
.info .sub { color:#7f8c8d; font-size: 14px; }
.menu { margin-top: 12px; display:flex; flex-direction:column; gap:8px; }
.menu-item { background:#fff; padding:12px; border-radius:8px; border:1px solid #eee; }
</style>