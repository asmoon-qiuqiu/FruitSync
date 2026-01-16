<script setup>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'
  import Top from './components/Top.vue'
</script>

<template>
  <div id="app">
    <!-- 全局头部 -->
    <Header></Header>
    <!-- 页面路由渲染出口 -->
    <router-view></router-view>
    <!-- 全局底部 -->
    <Footer></Footer>
    <!-- 全局返回顶部 -->
    <Top></Top>
  </div>
</template>

<style lang="scss">
  /* 全局重置样式 */
  * {
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 0;
  }
</style>
