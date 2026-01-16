<script setup>
  import MainFruits from '@/views/home/MainFruits.vue'
</script>

<template>
  <!-- 轮播图 -->
  <div class="banner">
    <div
      id="carouselExampleFade"
      class="carousel slide"
      data-bs-ride="carousel"
      data-bs-interval="2000"
      data-bs-scroll="false"
    >
      <div class="carousel-inner">
        <!-- 轮播项图片替换 -->
        <div class="carousel-item active">
          <img
            src="../../../public/images/banner.jpg"
            class="d-block w-100"
            alt="水果轮播图1"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../../../public/images/banner2.jpg"
            class="d-block w-100"
            alt="水果轮播图2"
          />
        </div>
        <div class="carousel-item">
          <img
            src="../../../public/images/banner3.jpg"
            class="d-block w-100"
            alt="水果轮播图3"
          />
        </div>
      </div>
      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide="prev"
      >
        <span
          class="carousel-control-prev-icon"
          aria-hidden="true"
        ></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#carouselExampleFade"
        data-bs-slide="next"
      >
        <span
          class="carousel-control-next-icon"
          aria-hidden="true"
        ></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>

  <!-- 内容 -->
  <MainFruits></MainFruits>
</template>

<style scoped lang="scss">
  .banner {
    height: 500px !important;
    overflow: hidden;
    position: relative;
    min-height: 500px !important;
    max-height: 500px !important; // 严格限制最大高度
    display: block; // 改为 block，避免 flex 影响

    .carousel {
      height: 500px !important;
      min-height: 500px !important;
      max-height: 500px !important;
      margin: 0;
      padding: 0;
    }

    .carousel-inner {
      height: 500px !important;
      min-height: 500px !important;
      max-height: 500px !important;
      margin: 0;
      padding: 0;
      position: relative;
      overflow: hidden;
    }

    .carousel-item {
      height: 500px !important;
      min-height: 500px !important;
      max-height: 500px !important;
      margin: 0;
      padding: 0;
      // 关键修改：使用绝对定位让所有轮播项叠加
      position: absolute !important;
      top: 0;
      left: 0;
      width: 100%;

      // 确保切换过程中的状态也保持固定高度
      &.active {
        display: block !important;
        height: 500px !important;
      }
    }

    // 给轮播图片添加固定高度
    .carousel-item img {
      height: 607px !important;
      width: 100% !important;
      min-height: 607px !important;
      max-height: 607px !important;
      object-fit: cover;
      background-color: #f5f5f5;
      display: block !important; // 移除图片底部间隙
      margin: 0;
      padding: 0;
    }

    .carousel-control-prev,
    .carousel-control-next {
      width: 50px;
      height: 50px;
      top: 50%;
      transform: translateY(-50%);
      background-color: rgba(255, 255, 255, 0.6);
      border-radius: 50%;
      padding: 0;
      margin: 0 5px 0 0;
      z-index: 10; // 确保按钮在最上层

      .carousel-control-prev-icon,
      .carousel-control-next-icon {
        width: 25px;
        height: 20px;
        background-size: 100%;
      }
    }

    @media screen and (max-width: 768px) {
      display: none;
    }
  }
</style>
