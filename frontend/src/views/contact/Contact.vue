<script setup>
  import TxMap from '@/components/TxMap.vue'
</script>

<template>
  <div class="contact">
    <div class="contact-mask">
      <div class="contact-content">
        <h4>联系方式</h4>
        <h6>网站问题&建议意见</h6>
        <p>Email：2371824615@qq.com</p>
        <p>QQ：2371824615</p>
        <hr />
      </div>
      <div class="contact-content">
        <h6>微信</h6>
        <img
          src="@public/images/wx.jpg"
          alt="微信"
        />
        <hr />
      </div>
      <div class="contact-content">
        <h6>地址</h6>
        <TxMap></TxMap>
        <hr />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  $primary-color: #fff0f5; // 主题颜色变量
  $minor-color: #c2185b;
  .contact {
    min-height: calc(100vh - 176px);
    background: url('@public/images/banner3.jpg') no-repeat center;
    background-size: cover;
    background-attachment: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-flow: column wrap; // 子元素垂直排列并在需要时换行

    .contact-mask {
      background: rgba(253, 231, 233, 0.8);
      width: 50%;
      padding: 10px;
      margin: 20px 0;
      overflow: auto;
      .contact-content {
        color: $minor-color;
        padding: 10px;
        h4 {
          margin-bottom: 15px;
        }
        hr {
          width: 100%;
        }
        p {
          text-indent: 1em;
          line-height: 16px;
        }
        img {
          width: 200px;
          height: 200px;
          display: block;
          margin-top: 10px;
        }
      }
    }
  }
  // 原样式保持不变，新增以下媒体查询
  @media screen and (max-width: 768px) {
    .contact {
      // 移动端调整最小高度（适配不同导航栏高度）
      min-height: calc(100vh - 61px);
      padding: 65px 0; // 留出高度，避免内容被遮挡
      .contact-mask {
        width: 90%;
        margin: 10px 0;
        padding: 10px 0;
        .contact-content {
          padding: 8px; // 减少内容区内边距

          h4 {
            font-size: 18px;

            h6 {
              font-size: 14px;
            }

            p {
              font-size: 13px;
              line-height: 1.6;
              margin: 0;
            }

            img {
              width: 150px;
              height: 150px;
            }
          }
        }
      }
    }
  }
</style>
