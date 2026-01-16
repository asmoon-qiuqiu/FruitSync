<script setup>
  import { ref, onMounted, onUnmounted } from 'vue'

  // 1.控制返回顶部按钮显示/隐藏的状态（默认隐藏）
  const showBackTop = ref(false)

  // 滚动到顶部的方法
  const scrollToTop = () => {
    window.scrollTo({
      top: 0, // 滚动到页面顶部
      behavior: 'smooth', // 平滑滚动效果
    })
  }

  // 监听页面滚动事件的处理函数
  const handleScroll = () => {
    // 当页面滚动距离顶部超过 150px 时，显示按钮
    showBackTop.value = window.pageYOffset > 150
  }

  // 页面挂载时添加滚动监听
  onMounted(() => {
    window.addEventListener('scroll', handleScroll)
  })

  // 页面卸载时移除滚动监听（避免内存泄漏）
  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
</script>

<template>
  <!-- 返回顶部按钮：默认隐藏，滚动到指定高度显示 -->
  <button
    class="back-to-top"
    v-show="showBackTop"
    @click="scrollToTop"
  >
    <div class="tooltip-text">
      <!-- 上方弹出的文字提示 -->
      <span class="text">返回顶部</span>
      <i class="bi bi-arrow-up"></i>
    </div>
  </button>
</template>

<style lang="scss">
  /* 返回顶部按钮样式 */
  .back-to-top {
    position: fixed; // 固定定位，不随页面滚动
    bottom: 30px; // 距离页面底部 30px
    right: 30px; // 距离页面右侧 30px
    width: 45px;
    height: 45px;
    border-radius: 50%; // 圆形按钮
    background-color: #fff0f5; // 与头部同色系，保持风格统一
    border: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); // 阴影增强层次感
    cursor: pointer;
    transition: background-color 0.3s; //  hover 过渡效果
    z-index: 10000; // 确保按钮在最上层
    &:hover {
      background-color: #c2185c9c; //  hover 时加深颜色
    }

    // 上方文字
    .tooltip-text {
      position: relative;

      .bi {
        font-size: 20px; // 图标大小
      }

      .text {
        position: absolute;
        bottom: 35px;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
        margin-bottom: 10px;
        font-size: 14px;
        background-color: #c2185b;
        color: white;
        border-radius: 4px;
        padding: 4px 8px;
        pointer-events: none;
        opacity: 0;
        transition: all 0.3s ease;

        &::after {
          content: '';
          position: absolute;
          top: 100%;
          left: 50%;
          transform: translateX(-50%);
          border-width: 5px;
          border-style: solid;
          border-color: #c2185b transparent transparent transparent;
        }
      }
    }

    &:hover .text {
      opacity: 1;
    }

    &:hover .bi {
      color: #fff;
    }
  }

  @media screen and (max-width: 768px) {
    /* 小屏幕下“返回顶部”按钮优化 */
    .back-to-top {
      width: 30px;
      height: 30px;
      bottom: 10%;
      right: 20px;

      .bi {
        font-size: 12px;
      }

      .text {
        display: none;
      }
    }
  }
</style>
