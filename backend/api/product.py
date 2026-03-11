"""
商品管理API路由
功能：提供商品的增删改查接口，支持分页查询
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlmodel import Session, select, func
import math
import logging

from model.product import Product
from schemas.products.product import (
    ProductResponse,
    ProductListResponse,
)
from database import get_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["products"])


@router.get(
    "/products",
    response_model=ProductListResponse,
    status_code=status.HTTP_200_OK,
    summary="获取商品列表（分页）接口",
    description="获取所有商品列表，支持分页查询",
)
async def get_products(
    session: Annotated[Session, Depends(get_session)],
    page: Annotated[int, Query(ge=1, description="页码，从1开始")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="每页数量，最大100")] = 6,
    category: Annotated[str | None, Query(description="商品分类筛选")] = None,
    search: Annotated[str | None, Query(description="商品名称模糊搜索关键词")] = None,
):
    try:
        """获取商品列表（带分页）"""
        logger.info(
            f"开始查询商品列表 - 页码：{page}，每页数量：{page_size}，分类：{category}，搜索关键词：{search}"
        )
        # 构建查询语句
        statement = select(Product)

        # 如果有分类筛选
        if category:
            statement = statement.where(Product.category == category)

        # 名称模糊搜索（不区分大小写，适配PostgreSQL/MySQL）
        if search and search.strip():
            # MySQL 用 like，PostgreSQL 用 ilike
            statement = statement.where(Product.name.like(f"%{search.strip()}%"))
            logger.debug(
                f"添加名称搜索条件：{search.strip()}"
            )  # 调试日志：记录搜索关键词

        # 只显示有库存的商品
        statement = statement.where(Product.in_stock == True)

        # 按id排列
        statement = statement.order_by(Product.id.asc())
        # statement = statement.order_by(Product.id.desc())

        # 获取总数
        count_statement = select(func.count(Product.id))
        if category:
            count_statement = count_statement.where(Product.category == category)

        if search and search.strip():
            count_statement = count_statement.where(
                Product.name.like(f"%{search.strip()}%")
            )

        count_statement = count_statement.where(Product.in_stock == True)
        total = await session.scalar(count_statement) or 0
        logger.debug(f"符合条件的商品总数：{total}")  # 调试日志：记录总数

        # 计算总页数
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # 分页查询
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)
        logger.debug(
            f"分页参数 - 偏移量：{offset}, 每页数量：{page_size}"
        )  # 调试日志：记录分页参数

        # 执行分页查询语句，获取当前页的商品数据库模型列表
        # session.exec(statement) 执行构造好的SQL查询，返回结果集对象
        # .all() 将结果集转换为包含Product（数据库模型）实例的列表
        products = (await session.exec(statement)).all()
        logger.debug(
            f"当前页查询到的商品数量：{len(products)}"
        )  # 调试日志：记录当前页商品数量

        # 将数据库模型列表转换为响应模型列表（核心：类型适配+数据校验）
        # 遍历每一个数据库查询得到的Product实例，逐个转换为对外输出的ProductResponse响应模型
        # model_validate：Pydantic v2核心方法，自动校验数据并完成模型转换，确保输出格式符合接口定义
        product_response = [
            ProductResponse.model_validate(product.model_dump()) for product in products
        ]  # 转换为响应模型列表
        # 记录查询成功日志
        logger.info(
            f"商品列表查询成功 - 总数量：{total}，总页数：{total_pages}，当前页返回数量：{len(product_response)}"
        )
        return ProductListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            products=product_response,
        )
    # 异常处理+日志记录
    except HTTPException:
        # 主动抛出的HTTP异常（如参数校验失败），直接向上抛出
        session.rollback()  # 回滚数据库事务，确保数据一致性
        raise
    except Exception as e:
        # 未知异常：记录错误日志（包含详细堆栈），并返回500错误
        logger.error(
            f"商品列表查询失败 - 页码：{page}，每页数量：{page_size}，错误信息：{str(e)}",
            exc_info=True,  # 记录完整的异常堆栈，便于排查问题
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，获取商品列表失败，请稍后重试",
        )
