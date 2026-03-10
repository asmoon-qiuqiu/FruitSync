<template>
  <div class="footer">
    <div class="footer-content">
      <p class="footer-addr">地址: 广东省惠州市惠东县黄埠镇</p>
      <p class="footer-email">联系邮箱: 2371824615@qq.com</p>
      <p class="footer-copyright">© 2025 个人制作 版权所有</p>
    </div>
  </div>

  <!-- 小屏幕底部导航 -->
  <div class="mini-footer">
    <router-link
      to="/"
      class="nav-item"
    >
      <i class="bi bi-house"></i>
      <p>首页</p>
    </router-link>

    <router-link
      to="/myinfo"
      class="nav-item"
    >
      <i class="bi bi-person-circle"></i>
      <p>我的</p>
    </router-link>
  </div>
</template>

<style scoped lang="scss">
  .footer {
    background-color: #fff0f5;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 20px 10px;
    opacity: 0.85;
    transition: opacity 0.3s ease;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);

    &:hover {
      opacity: 1;
    }

    .footer-content {
      /* 限制最大宽度，大屏下不拉伸 */
      max-width: 1200px;
      margin: 0 auto;
      text-align: center;

      /* 地址文字样式 */
      .footer-addr {
        color: #c2185b;
        font-size: 16px;
        margin-bottom: 10px;
      }

      /* 邮箱文字样式 */
      .footer-email {
        color: #c2185b;
        font-size: 16px;
        margin-bottom: 10px;

        /* 邮箱hover时变色，增加交互感 */
        &:hover {
          color: #8d6e63;
          cursor: pointer;
        }
      }

      /* 版权信息样式 */
      .footer-copyright {
        color: #c2185b;
        /* 稍浅灰色，区分主次信息 */
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: -10px;
      }
    }
  }

  /* 响应式适配：小屏幕下调整文字大小和内边距 */
  @media screen and (max-width: 768px) {
    .footer {
      display: none;
    }

    .mini-footer {
      background-color: #fff0f5;
      position: fixed;
      display: flex;
      justify-content: space-around;
      align-items: center;
      left: 0;
      bottom: 0;
      width: 100%;
      z-index: 1001;
      .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #333;
        text-decoration: none;

        &.router-link-active {
          color: #c2185b; // 激活时变色
        }
      }

      .bi {
        font-size: 24px;
        margin-top: 4px;
      }

      p {
        font-size: 14px;
        margin: 0;
      }
    }
  }

  @media screen and (min-width: 769px) {
    .mini-footer {
      display: none;
    }
  }
</style>
