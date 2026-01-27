import service from "@/utils/request";

/**
 * 获取商品列表（分页）,仅返回有库存的商品，支持分类筛选
 * @param {Object} params - 请求参数（GET查询参数）
 * @param {number} [params.page=1] - 页码，从1开始
 * @param {number} [params.page_size=6] - 每页数量-默认6，范围1-100
 * @param {string} [params.category] - 可选，商品分类筛选（如"水果/家电/服饰"）
 * @returns {Promise} - 返回商品列表数据（包含列表数组、总数等）
 */
export const getProductListApi = (params) => { // 设置默认空对象
    return service({
        url: "/api/products",
        method: "GET",
        params, //传递查询参数

    });
};
