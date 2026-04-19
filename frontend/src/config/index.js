// 后端FastAPI的基础地址
// 注意：如果后端部署在不同的地址或端口，请修改此处
// // 开发环境使用本地地址
// export const BASE_API_URL = 'http://localhost:8000'

// // // 后端FastAPI生产的基础地址
// export const BASE_API_URL = ''

const env = import.meta.env.MODE;
export const BASE_API_URL = env === 'production' ? '' : import.meta.env.VITE_API_BASE_URL;