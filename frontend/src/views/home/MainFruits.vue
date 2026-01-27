<script setup>
  import { ref, computed, watch, onMounted } from 'vue'
  import { getProductListApi } from '@/api/product'
  import { ElMessage } from 'element-plus'
  import { useRoute, useRouter } from 'vue-router'
  import { BASE_API_URL } from '@/config' // 导入后端基础URL

  // 路由实例
  const route = useRoute()
  const router = useRouter()

  // 1.分页按钮相关逻辑和存储接口返回的商品数据和分页信息
  const jumpPageInput = ref('') //用于存储跳转输入框的值
  const currentPage = ref(1) // 当前页码
  const pageSize = ref(6) // 每页显示数量
  const total = ref(0) // 总记录数
  const totalPages = ref(1) // 总页数
  const currentCategory = ref('') // 当前选中的分类（默认空，查询所有）
  const productList = ref([]) // 商品列表数据
  const loading = ref(false) // 加载状态

  // 搜索关键词（从URL参数获取）
  const searchKeyword = ref(route.query.search || '')
  // 搜索状态标识
  const isSearching = ref(false)
  // 统一清空搜索方法
  const clearSearch = () => {
    searchKeyword.value = ''
    isSearching.value = false
    currentPage.value = 1
    router.push({ query: { ...route.query, search: undefined } })
  }
  // 获取商品列表数据函数
  const getProductList = async () => {
    loading.value = true
    try {
      // 调用接口，传递分页和分类参数
      const response = await getProductListApi({
        page: currentPage.value,
        page_size: pageSize.value, // 每页数量
        category: currentCategory.value || undefined, // 分类为空时不传该参数
        search: searchKeyword.value.trim() || undefined, // 传递搜索参数-搜索关键词为空时不传该参数
      })
      console.log('完整响应对象:', response)
      // 解构接口返回的分页数据
      productList.value = response.data.products || []
      total.value = response.data.total || 0
      totalPages.value = response.data.total_pages || 1
    } catch (error) {
      console.error('获取商品列表失败：', error)
      productList.value = []
      total.value = 0
      totalPages.value = 1
      ElMessage.error('商品加载失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }
  // 直接返回接口获取的当前页数据（后端已做分页）
  const FruitsList = computed(() => {
    return productList.value.map((fruit) => ({
      id: fruit.id,
      name: fruit.name,
      desc: fruit.description, // 后端字段为description,映射前端的desc
      price: fruit.price,
      // 拼接完整的图片url，BASE_API_URL + 后端返回的相对路径
      image: fruit.image_url ? `${BASE_API_URL}${fruit.image_url}` : '', // 后端字段为image_url,映射前端的image
    }))
  })

  // 分类切换函数（绑定到分类按钮）
  const changeCategory = (category) => {
    currentCategory.value = category
    clearSearch() // 切换分类时清空搜索状态
    getProductList()
  }

  // 切换页码
  const changePage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page // 转递新的页码
      jumpPageInput.value = '' // 跳转后清空输入框
      getProductList() // 切换页码后重新请求接口获取数据
      // 切换页码后滚动到水果列表顶部
      const fruitList = document.querySelector('.fruit-list')
      if (fruitList) {
        fruitList.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }
  }
  // 页码跳转处理函数
  const handleJumpPageInput = () => {
    const page = parseInt(jumpPageInput.value)
    if (!isNaN(page)) {
      changePage(page)
    }
  }
  // 生成页码数组（最多显示5个页码）
  const pageNumbers = computed(() => {
    const pages = [] // 存储最终要渲染的分页页码数组（包含数字和省略号）
    const total = totalPages.value // 总页数（响应式数据）
    const current = currentPage.value // 当前页码（响应式数据）

    // 场景1：总页数≤5，无需省略号，直接显示所有页码（1~total）
    if (total <= 5) {
      for (let i = 1; i <= total; i++) {
        pages.push(i)
      }
    } else {
      // 场景2：总页数>5，需要显示省略号优化分页展示
      if (current <= 3) {
        // 子场景2.1：当前页在最前面（≤3），显示前4页 + 省略号 + 最后1页（如：1,2,3,4,...,10）
        pages.push(1, 2, 3, 4, '...', total)
      } else if (current >= total - 2) {
        // 子场景2.2：当前页在最后面（≥total-2），显示第1页 + 省略号 + 最后4页（如：1,...,7,8,9,10）
        pages.push(1, '...', total - 3, total - 2, total - 1, total)
      } else {
        // 子场景2.3：当前页在中间，显示第1页 + 省略号 + 当前页前后1页 + 省略号 + 最后1页（如：1,...,5,6,7,...,10）
        pages.push(1, '...', current - 1, current, current + 1, '...', total)
      }
    }
    return pages // 返回最终的分页页码数组，用于页面渲染
  })

  // 图片加载失败的处理函数
  const handleImageError = (e) => {
    // 图片加载失败时显示兜底图
    e.target.src = `${BASE_API_URL}/images/default.jpg`
    // 也可以隐藏图片：e.target.style.display = 'none'
  }

  // 第一个watch：监听分页、分类参数变化（原有逻辑，保留不变）
  watch(
    [currentPage, pageSize, currentCategory],
    () => {
      getProductList()
    },
    { immediate: false }, // 避免首次重复请求
  )

  // 第二个watch：单独监听URL中search参数变化（新增的搜索监听，与上面平级）
  watch(
    () => route.query.search, // 监听URL中的search查询参数
    (newSearch) => {
      searchKeyword.value = newSearch || '' // 更新本地搜索关键词
      isSearching.value = !!searchKeyword.value.trim() // 更新搜索状态标识
      currentPage.value = 1 // 搜索参数变化，强制重置到第一页
      getProductList() // 重新请求商品列表
    },
    { immediate: true }, // 立即执行：组件挂载时就触发一次，适配初始的URL搜索参数
  )
  // 页面挂载时首次加载数据
  onMounted(() => {
    getProductList()
  })
</script>

<template>
  <div class="main">
    <div class="tab">
      <h2>水果目录</h2>
      <!-- 新增：搜索状态提示栏 -->
      <div
        v-if="isSearching"
        class="search-tip"
        style="padding: 8px; text-align: center; color: #c2185b; font-weight: 500"
      >
        🔍 正在搜索：{{ searchKeyword }}
        <button
          @click="clearSearch"
          style="
            margin-left: 8px;
            padding: 2px 6px;
            border: 1px solid #c2185b;
            border-radius: 4px;
            background: #fff;
            color: #c2185b;
            cursor: pointer;
            font-size: 14px;
          "
        >
          清空
        </button>
      </div>
      <!-- 分类按钮 -->
      <button
        class="tablinks"
        @click="changeCategory('')"
      >
        全部水果
      </button>
      <button
        class="tablinks"
        @click="changeCategory('苹果')"
      >
        苹果
      </button>
      <button
        class="tablinks"
        @click="changeCategory('香蕉')"
      >
        香蕉
      </button>
      <button
        class="tablinks"
        @click="changeCategory('西瓜')"
      >
        西瓜
      </button>
      <button
        class="tablinks"
        @click="changeCategory('橙子')"
      >
        橙子
      </button>
      <button
        class="tablinks"
        @click="changeCategory('葡萄')"
      >
        葡萄
      </button>
    </div>

    <!-- 商品列表 -->
    <div class="fruit-list">
      <!-- 加载状态提示 -->
      <div
        v-if="loading"
        class="loading"
      >
        加载中...
      </div>
      <!-- 空数据提示 -->
      <div
        v-else-if="productList.length === 0"
        class="empty"
      >
        {{
          isSearching
            ? currentCategory
              ? `未找到"${searchKeyword}"相关的【${currentCategory}】商品`
              : `未找到"${searchKeyword}"的商品`
            : currentCategory
              ? `暂无【${currentCategory}】相关商品`
              : '暂无商品数据'
        }}
      </div>
      <ul v-else>
        <li
          class="list"
          v-for="fruit in FruitsList"
          :key="fruit.id"
        >
          <div class="fruit-card">
            <img
              :src="fruit.image"
              :alt="fruit.name"
              class="fruit-img"
              @error="handleImageError"
            />

            <div class="fruit-info">
              <h3>{{ fruit.name }}</h3>
              <p>{{ fruit.desc }}</p>
              <span class="price">¥{{ fruit.price }}/斤</span>
            </div>
          </div>
        </li>
      </ul>

      <!-- 分页模块 -->
      <div
        class="pagination"
        v-if="total > 0"
      >
        <!-- 上一页 -->
        <button
          class="page-btn"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          <i class="bi bi-chevron-left"></i>
        </button>
        <!-- 页码 -->
        <button
          class="page-number"
          v-for="(page, index) in pageNumbers"
          :class="{ active: page === currentPage, ellipsis: page === '...' }"
          :disabled="page === '...'"
          :key="index"
          @click="page !== '...' && changePage(page)"
        >
          {{ page }}
        </button>
        <!-- 下一页 -->
        <button
          class="page-btn"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          <i class="bi bi-chevron-right"></i>
        </button>
        <!-- 跳转输入框 -->
        <div class="page-jump">
          <span>跳转到</span>
          <input
            type="number"
            min="1"
            :max="totalPages"
            v-model="jumpPageInput"
            @keyup.enter="handleJumpPageInput"
          />
          <span>页</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
  // 加载/空数据样式
  .loading {
    text-align: center;
    padding: 20px;
    color: #c2185b;
    font-size: 16px;
  }
  .empty {
    text-align: center;
    padding: 20px;
    color: #c2185b;
    font-size: 24px;
    font-weight: bold;
  }
  .main {
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start; // 顶部对齐
    padding-left: 10px;
    background: url(../../public/images/main.jpg) no-repeat center;
    background-size: cover;
    background-attachment: fixed;

    h2 {
      color: #c2185b;
      margin: 15px 0;
      padding-left: 5px;
    }

    .tab {
      flex: 0 0 15%;
      border: 1px solid #e0f2e9;
      background-color: #fff0f5;
      height: auto;
      margin-top: 20px;
      margin-bottom: 20px;
      padding: 0 5px;
      opacity: 0.9;

      .tablinks {
        display: block;
        background-color: #fff;
        color: #f97316;
        padding: 20px 15px;
        width: 100%;
        border: none;
        text-align: center;
        transition: 0.3s;
        font-size: 18px;
        margin: 10px 0;
        border-radius: 5px;
        cursor: pointer;

        &:hover {
          background-color: #fff7ed;
          color: #ea580c;
        }

        &:active {
          background-color: #f97316;
          color: #fff;
        }
      }
    }

    .fruit-list {
      flex: 1;
      padding: 0 20px 20px 20px;

      margin-top: 20px;

      ul {
        padding: 0;
        display: grid; // 网格布局
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;

        .list {
          list-style-type: none;
          width: 100%;

          .fruit-card {
            border: 1px solid #eee;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

            .fruit-info {
              padding: 0 0 10px 10px;

              h3 {
                font-size: 20px;
                margin-top: 10px;
              }

              p {
                font-size: 14px;
                margin: 0;
              }
            }

            .fruit-img {
              width: 100%;
              height: 250px;
              object-fit: cover;
              border-radius: 5px;
            }
          }
        }
      }
    }

    // 分页样式
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 40px;
      padding: 20px 0;

      .page-btn,
      .page-number {
        min-width: 40px;
        height: 40px;
        border: 1px solid #ddd;
        background-color: #fff;
        color: #c2185b;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
        font-size: 14px;

        &:hover:not(:disabled):not(.ellipsis) {
          background-color: #c2185b;
          border-color: #c2185b;
          color: #fff;
        }

        &:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

        &.active {
          background-color: #c2185b;
          color: #fff;
          border-color: #c2185b;
        }

        &.ellipsis {
          border: none;
          cursor: default;
          background: transparent;
        }
      }

      .page-jump {
        display: flex;
        align-items: center;
        gap: 5px;
        margin-left: 15px;
        font-size: 14px;
        color: #c2185b;

        input {
          width: 40px;
          height: 20px;
          border: 1px solid #ddd;
          border-radius: 4px;
          text-align: center;
          font-size: 14px;
          outline: none;

          &:focus {
            border-color: #c2185b;
          }

          // 移除数字输入框的上下箭头
          &::-webkit-inner-spin-button,
          &::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
          }
        }
      }
    }
  }
  @media screen and (max-width: 1200px) {
    .main {
      padding: 0;
      .tab {
        display: flex;
        flex: 0 0 100%;
        flex-wrap: wrap;
        margin-top: 0;

        h2 {
          width: 100%;
          white-space: nowrap;
          padding-left: 5px;
          margin: 20px 0;
        }

        .tablinks {
          display: flex;
          justify-content: center;
          align-items: center;
          min-width: 120px;
          flex: 1 1 calc(25% - 10px);
          height: 50px;
          margin: 5px;
        }
      }

      .rside {
        flex: 0 0 100%;
        margin-bottom: 10px;
      }

      .fruit-list {
        padding: 10px;

        ul {
          grid-template-columns: repeat(2, 1fr);
          padding: 5px;
        }
      }
    }
  }

  @media screen and (max-width: 768px) {
    .main {
      padding-top: 45px;
      min-height: calc(100vh - 45px - 60px);
      .fruit-list {
        padding: 0 5px;
        margin-bottom: 0px;
        min-height: calc(100vh - 150px);
        ul {
          grid-template-columns: repeat(2, 1fr);
          gap: 5px;
          padding: 0;
          margin: 0;

          .list .fruit-card {
            margin: 0 5px 0 5px;

            .fruit-img {
              width: 100%;
              height: auto;
              object-fit: cover;
              border-radius: 4px;
            }

            .fruit-info {
              h3 {
                font-size: 14px;
                font-weight: bold;
              }

              p {
                font-size: 12px;
                font-weight: bold;
              }

              .price {
                font-size: 12px;
                padding-left: 2px;
                font-weight: bold;
              }
            }
          }
        }
      }

      // 分页
      .pagination {
        flex-wrap: wrap;
        margin-top: 10px;
        margin-bottom: 50px;

        .page-btn,
        .page-number {
          min-width: 30px;
          height: 30px;
          font-size: 12px;
        }

        .page-jump {
          font-size: 12px;
          margin-left: 5px;
        }
      }

      .rside {
        margin-bottom: 100px;
      }
    }
  }
</style>
