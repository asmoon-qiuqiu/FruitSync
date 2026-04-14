<template>
  <div class="footer">
    <div class="footer-content">
      <p class="footer-addr">地址: 广东省惠州市惠东县黄埠镇</p>
      <p class="footer-email">联系/投诉邮箱: 2371824615@qq.com</p>
      <p class="footer-copyright">© 2025 个人制作 asmoon版权所有</p>
      <!-- 备案号放在版权下面，不要加额外p标签 -->
      <a href="https://beian.miit.gov.cn/" target="_blank" class="footer-beian">粤ICP备2026038345号</a>
    </div>
  </div>

  <!-- 小屏幕底部导航 -->
  <!-- <div class="mini-footer">
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
  </div> -->
</template>

<style scoped lang="scss">
  .footer {
    background-color: #fff0f5;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 15px 10px;
    opacity: 0.85;
    transition: opacity 0.3s ease;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);

    &:hover {
      opacity: 1;
    }

    .footer-content {
      max-width: 1200px;
      margin: 0 auto;
      text-align: center;

      .footer-addr {
        color: #c2185b;
        font-size: 16px;
        margin-bottom: 6px; 
      }

      .footer-email {
        color: #c2185b;
        font-size: 16px;
        margin-bottom: 6px; 

        &:hover {
          color: #8d6e63;
          cursor: pointer;
        }
      }

      .footer-copyright {
        color: #c2185b;
        font-size: 14px;
        margin: 5px 0; 
      }

      /* 备案号样式 */
      .footer-beian {
        color: #c2185b;
        font-size: 14px;
        display: block; /* 独占一行 */
        margin-top: 8px;
        text-decoration: none; /* 去除默认下划线 */
        
        &:hover {
          text-decoration: underline; /* hover 加下划线 */
        }
      }
    }
  }

  @media screen and (max-width: 768px) {
    .footer {
      display: none;
    }
  }
</style>