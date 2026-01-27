<script setup>
  import { computed, ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import { getProductListApi } from '@/api/product'
  import Loading from './Loading.vue'
  import { ElMessage } from 'element-plus'
  const userStore = useUserStore() // 创建仓库实例
  const router = useRouter()
  const isLoading = ref(false) // 控制loading显示/隐藏
  // 1.搜索框逻辑
  const searchQuery = ref('') // 输入值
  const showSuggestions = ref(false) // 控制是否显示建议框
  const showSearchActive = ref(false) // 控制搜索框是否展开
  const allSuggestions = ref([]) // 所有数据
  // 2.小屏幕控制菜单显示|隐藏
  const isMenuOpen = ref(false) // 抽屉是否打开-默认关闭
  const isMenuVisible = ref(false) // 控制小屏幕抽屉菜单栏

  // 获取搜索建议（商品名称列表）
  const getAllSuggestions = async () => {
    try {
      isLoading.value = true
      const response = await getProductListApi()
      if (response.status === 200) {
        allSuggestions.value = Array.isArray(response.data.products) ? response.data.products : []
      }
      console.log('搜索数据', allSuggestions.value)
    } catch (error) {
      ElMessage.error('搜索失败')
      allSuggestions.value = []
    } finally {
      isLoading.value = false
    }
  }
  // 计算属性：根据输入过滤建议
  const filterSuggestions = computed(() => {
    if (!searchQuery.value.trim()) {
      return []
    } else {
      return allSuggestions.value.filter((item) => {
        if (typeof item === 'object' && item !== null && typeof item.name === 'string') {
          return item.name.includes(searchQuery.value)
        } else {
          return false
        }
      })
    }
  })

  // 点击建议项
  const selectSuggestion = (item) => {
    searchQuery.value = item.name
    showSuggestions.value = false // 隐藏建议框
    showSearchActive.value = true // 保持搜索框展开
    handleSearch() // 选中建议选项后直接搜索
  }
  // 搜索提交核心方法（跳转到首页并携带搜索参数）
  const handleSearch = () => {
    const keyWord = searchQuery.value.trim()
    if (keyWord) {
      router.push({ path: '/', query: { search: keyWord } }) // URL拼接?search=关键词
      showSuggestions.value = false // 隐藏建议框
      showSearchActive.value = true // 保持搜索框展开
      searchQuery.value = '' // 清空搜索框
    }
  }
  // 处理input获得焦点时建议框和输入框展开
  const handleFocus = () => {
    showSuggestions.value = true
    showSearchActive.value = true
  }
  // 处理input失去焦点时建议框隐藏，输入框展开
  const handleBlur = () => {
    setTimeout(() => {
      showSuggestions.value = false
      // 如果有搜索内容保持展开，否则收起
      if (!searchQuery.value.trim()) {
        showSearchActive.value = false
      }
    }, 200)
  }

  // 退出登录方法 ✨
  const handleLogout = () => {
    userStore.logout() // 调用Pinia的logout方法清除状态
    ElMessage.success('退出成功')
    router.push('/') // 跳转到登录页
  }

  // 小屏幕菜单打开和关闭按钮逻辑
  const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
    if (isMenuOpen.value) {
      // 打开时显示元素
      isMenuVisible.value = true
    } else {
      // 关闭时，等动画结束（300ms 对应动画时长）再隐藏
      setTimeout(() => {
        isMenuVisible.value = false
      }, 300)
    }
  }
  // 组件挂载时调用接口加载数据
  onMounted(() => {
    getAllSuggestions()
  })
</script>

<template>
  <Loading :visible="isLoading" />
  <!-- 1. 小屏幕触发（仅在≤600px显示） -->
  <div class="mini-header-fixed">
    <div class="mini-header">
      <!-- 抽屉菜单按钮 -->
      <button
        class="menu-btn"
        @click="toggleMenu"
        v-show="!isMenuOpen"
      >
        <i class="bi bi-list"></i>
      </button>

      <!-- 抽屉关闭按钮 -->
      <button
        class="close-btn"
        @click="toggleMenu"
        v-show="isMenuOpen"
      >
        <i class="bi bi-x"></i>
      </button>

      <!-- 2. 小屏幕侧边抽屉（从右侧弹出，≤600px显示） -->
      <div
        class="mobile-menu"
        :class="{ open: isMenuOpen, close: !isMenuOpen }"
        v-show="isMenuVisible"
      >
        <!-- 抽屉菜单内容 -->
        <div class="menu-content">
          <router-link
            to="/"
            @click="toggleMenu"
            class="link"
          >
            首页
          </router-link>

          <router-link
            to="about"
            @click="toggleMenu"
            class="link"
          >
            关于此站
          </router-link>
          <router-link
            to="contact"
            @click="toggleMenu"
            class="link"
          >
            联系方式
          </router-link>
          <!-- 动态显示用户名/登录按钮 ✨ -->
          <div
            v-if="userStore.isLoggedIn"
            class="user-info link"
            @click="toggleMenu"
          >
            <span>{{ userStore.username }}</span>
            <button
              @click="handleLogout"
              class="logout-btn"
            >
              登出
            </button>
          </div>
          <router-link
            to="login"
            @click="toggleMenu"
            class="link"
            v-else
          >
            <i class="bi bi-box-arrow-in-right"></i>
            登录
          </router-link>
        </div>
      </div>
    </div>
  </div>

  <!-- 3. 大屏幕导航（原导航，≥601px显示） -->
  <div class="header">
    <router-link to="/">首页</router-link>
    <router-link to="about">关于此站</router-link>
    <router-link to="contact">联系方式</router-link>
    <!-- 动态显示用户名/登录按钮 -->
    <div
      v-if="userStore.isLoggedIn"
      class="user-info"
    >
      <span class="username">{{ userStore.username }}</span>
      <button
        @click="handleLogout"
        class="logout-btn"
      >
        登出
      </button>
    </div>
    <router-link
      to="login"
      v-else
    >
      <i class="bi bi-box-arrow-in-right">登录</i>
    </router-link>
    <!-- 搜索框 -->
    <div class="search">
      <div class="search-container">
        <form @submit.prevent="handleSearch">
          <input
            class="search-input"
            :class="{ active: showSearchActive }"
            type="text"
            placeholder="搜索.."
            name="search"
            v-model="searchQuery"
            @focus="handleFocus"
            @input="showSuggestions = true"
            @blur="handleBlur"
            @keyup.enter="handleSearch"
          />

          <button
            type="submit"
            @click="handleSearch"
          >
            <i class="bi bi-search"></i>
          </button>
        </form>

        <!-- 建议框 -->
        <ul
          class="suggestion-box"
          v-if="showSuggestions && filterSuggestions.length"
        >
          <li
            v-for="(item, index) in filterSuggestions"
            :key="index"
            @click="selectSuggestion(item)"
          >
            {{ item.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  .header {
    background-color: #fff0f5;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
    border-radius: 5px;
    .user-info {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 0 15px;
      color: #c2185b;
      .username {
        font-size: 18px;
      }
      .logout-btn {
        background: transparent;
        border: 1px solid #c2185b;
        color: #c2185b;
        border-radius: 4px;
        padding: 4px 8px;
        cursor: pointer;
        &:hover {
          background: #c2185b;
          color: #fff;
        }
      }
    }
    a {
      font-size: 18px;
      padding: 15px;
      text-decoration: none;
      color: #c2185b;

      .bi {
        margin-right: 5px;
      }

      &:hover,
      &:active {
        background-color: #c2185b;
        color: #f5f9ff;
      }
    }

    // 搜索样式
    .search {
      .search-container {
        position: relative;
        display: inline-block;

        // 建议框样式
        .suggestion-box {
          position: absolute;
          top: 100%;
          left: 0;
          width: 100%;
          background-color: #fff;
          border: 1px solid #ddd;
          border-radius: 0 0 6px 6px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
          z-index: 999;
          max-width: 200px;
          max-height: 200px;
          overflow: auto;

          li {
            list-style: none;
            padding: 8px;
            color: #de5b1a;
            cursor: pointer;
            transition: background 0.2s;
          }

          &:hover,
          li:hover {
            background: #fff0f5;
            color: #c2185b;
          }
        }

        // 默认隐藏input
        .search-input {
          padding: 8px;
          border: 1px solid #ddd;
          border-radius: 4px 0 0 4px;
          outline: none;
          font-size: 14px;
          color: #c2185b;
          max-width: 0;
          opacity: 0;
          transition: all 0.3s ease;

          &.active {
            max-width: 150px;
            opacity: 1;
          }
        }

        // 鼠标悬停或输入框获得焦点时 显示input
        form:hover .search-input,
        form:focus-within .search-input {
          max-width: 150px;
          opacity: 1;
        }

        button {
          padding: 8px 12px;
          background-color: #c2185cde;
          color: #fff;
          border: none;
          cursor: pointer;
          transition: background-color 0.3s;

          &:hover {
            background-color: #c2185b;
          }

          i {
            font-size: 14px;
          }
        }
      }
    }
  }

  @media screen and (max-width: 768px) {
    .header {
      display: none;
    }

    .mini-header-fixed {
      position: fixed;
      width: 100%;
      left: 0;
      top: 0;
      z-index: 1001;
      .mini-header {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        position: relative; // 为侧边抽屉做定位参考
        background-color: #fff0f5;
        // 菜单按钮样式
        .menu-btn {
          border: none;
          font-size: 24px;
          color: #fff0f5;
          background-color: #c2185b;
          padding: 5px;
          cursor: pointer;
        }

        // 关闭按钮样式
        .close-btn {
          border: none;
          font-size: 24px;
          color: #333;
          background-color: #fff0f5;
          padding: 5px;
          cursor: pointer;
          z-index: 999;
        }

        // 打开菜单动画
        @keyframes openMenu {
          from {
            transform: translateX(100%); //初始状态：完全在右侧外部
          }

          to {
            transform: translateX(0); //结束状态：滑入到正常位置
          }
        }

        @keyframes closeMenu {
          from {
            transform: translateX(0); //初始状态：完全在右侧外部
          }

          to {
            transform: translateX(100%); //结束状态：滑入到正常位置
          }
        }

        // 侧边抽屉
        .mobile-menu {
          position: absolute;
          width: 200px;
          height: calc(100vh - 61px);
          top: 0;
          right: 0; // 从右侧弹出
          background-color: #fff0f5;
          box-shadow: -20px 0 10px rgba(0, 0, 0, 0.1);
          //滑出动画
          animation-duration: 0.3s;
          animation-timing-function: ease;
          animation-iteration-count: 1;
          animation-fill-mode: forwards;
          z-index: 998;

          &.open {
            animation-name: openMenu;
            // 打开后允许点击
            pointer-events: auto;
          }

          &.close {
            animation-name: closeMenu;
            // 关闭后禁止点击（可选）
            pointer-events: none;
          }

          // 抽屉菜单内容
          .menu-content {
            display: flex;
            flex-direction: column;
            padding: 50px 30px 0 0;
            .user-info {
              display: flex;
              flex-direction: column;
              align-items: flex-start;
              gap: 5px;
              padding: 15px;
            }
            .logout-btn {
              border: 1px solid #fff0f5;
              margin-top: 5px;
              background-color: #fff0f5;
              color: #c2185b;
              &:hover {
                background-color: #c2185b;
                color: #fff;
              }
            }
            .link {
              font-size: 18px;
              padding: 15px;
              text-decoration: none;
              color: #c2185b;
            }
          }
        }
      }
    }
  }

  // 大屏幕隐藏小屏幕菜单容器
  @media screen and (min-width: 769px) {
    .mini-header {
      display: none;
    }
  }
</style>
