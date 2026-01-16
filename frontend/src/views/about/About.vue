<script setup></script>

<template>
  <div class="about">
    <div class="about-content">
      <h3>此站说明</h3>
      <div class="about-explanation">
        <p>
          此站是由个人
          <span class="user">
            (asmoon)
            <i class="bi bi-emoji-smile"></i>
          </span>
          独自开发维护的水果主题小站哦~旨在为用户提供第一时间的水果资讯和优质的水果购买体验。希望你们能够喜欢这个网站，并提供宝贵的反馈意见，让我们一起把它做得更好！
          <img
            class="manbo"
            src="../../../public/images/manbo2.gif"
            alt="曼波"
          />
        </p>

        <p>
          此外，此网站已在 GitHub 开源，欢迎大家前往查看代码。若遇到 BUG，可前往 GitHub
          反馈或贡献代码，也可跟我
          <span
            class="myself"
            @click="$router.push('/contact')"
          >
            个人联系
          </span>
          提出建议。
        </p>

        <p>祝大家预览愉快！</p>
      </div>

      <div class="about-github">
        <h3>
          速戳链接
          <span>👇</span>
        </h3>
        <p>
          - 码云项目仓库：
          <a
            class="github-link"
            href="https://gitee.com/qiuqiumoon/FruitSync"
            target="_blank"
          >
            https://gitee.com/qiuqiumoon/FruitSync
          </a>
        </p>
        <p>
          - GitHub项目仓库:
          <a
            class="github-link"
            href="https://github.com/asmoon-qiuqiu/FruitSync"
            target="_blank"
          >
            https://github.com/asmoon-qiuqiu/FruitSync
          </a>
        </p>
        <span>（点击链接即可跳转）</span>

        <img
          src="../../../public/images/contact.gif"
          alt="唠嗑~"
        />
      </div>

      <div class="about-contact">
        <h3>联系方式</h3>
        <p>
          欢迎唠嗑~~~ 要是有特别的想法想单独聊，直接去 GitHub 私信 asmoon
          就好啦，看到都会回复的~当然也可以通过如下方式👇
        </p>

        <button
          class="contact-btn"
          @click="$router.push('/contact')"
        >
          <span class="contact-text">联系方式</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  $primary-color: #fff0f5; // 主题颜色变量
  $minor-color: #c2185b;

  .about {
    min-height: calc(100vh - 176px);
    background: url('@public/images/about.jpg') no-repeat center;
    background-size: cover;
    background-attachment: fixed;
    padding: 10px;
    background-color: $minor-color;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-flow: column wrap; // 子元素垂直排列并在需要时换行
    .about-content {
      background: rgba(255, 240, 245, 0.3);
      width: 80%;
      padding: 10px;
      overflow: auto;
      h3 {
        margin-top: 10px;
        color: $minor-color;
        span {
          font-size: 20px;
        }
      }

      .about-explanation {
        .user {
          color: $primary-color;
          font-weight: bold;
        }
        .myself {
          color: $minor-color;
          font-weight: bold;
          text-decoration: underline solid;
          cursor: pointer;
        }
        .manbo {
          float: right;
          border: 1px solid #b0938d;
          border-radius: 50px;
          width: 100px;
          height: 100px;
          margin-right: 30px;
          margin-top: 20px;
        }
      }

      .about-github {
        img {
          float: right;
          width: 150px;
          height: 150px;
        }
        .github-link {
          color: $primary-color;
          font-size: 18px;
          text-decoration: none;
          &:hover {
            color: $minor-color;
            cursor: pointer;
          }
        }
      }
      .about-contact {
        .contact-btn {
          border: none;
          padding: 15px;
          margin: 0 auto;
          display: block; // 确保按钮是块级元素，margin生效
          background-color: $minor-color;
          color: #ffb7b2;
          border-radius: 8px;
          cursor: pointer;
          // 定义动画关键帧
          @keyframes changeText {
            0% {
              color: #ffb7b2;
            }
            50% {
              color: #ffb74d;
            }
            100% {
              color: $primary-color;
            }
          }
          &-text {
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            animation: changeText 3s ease-in-out infinite;
          }
          &:hover {
            background-color: #d83a6e;
          }
        }
      }
    }
  }

  @media screen and (max-width: 768px) {
    .about {
      min-height: calc(100vh - 61px);
      padding: 65px 0; // 留出高度，避免内容被遮挡/
      p {
        margin: 0;
      }
      .about-content {
        .about-explanation {
          .manbo {
            width: 100px;
            height: 100px;
            margin: 0;
          }
        }
        .about-github {
          img {
            width: 100px;
            height: 100px;
          }
        }
        .about-contact {
          .contact-btn {
            margin-top: 10px;
            padding: 10px;
            .contact-text {
              font-size: 14px;
            }
          }
        }
      }
    }
  }
</style>
