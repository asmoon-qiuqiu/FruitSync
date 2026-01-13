"""
商品管理API路由
功能：提供商品的增删改查接口，支持分页查询
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from datetime import datetime
import math

from model.product import Product
from schemas.products.product import (
    ProductResponse,
    ProductListResponse,
    ProductCreateRequest,
)
from database import get_session

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
):
    """获取商品列表（带分页）"""
    # 构建查询语句
    statement = select(Product)

    # 如果有分类筛选
    if category:
        statement = statement.where(Product.category == category)

    # 只显示有库存的商品
    statement = statement.where(Product.in_stock == True)

    # 按id排列
    statement = statement.order_by(Product.id.asc())
    # statement = statement.order_by(Product.id.desc())

    # 获取总数
    count_statement = select(func.count(Product.id))
    if category:
        count_statement = count_statement.where(Product.category == category)
    count_statement = count_statement.where(Product.in_stock == True)

    total = await session.scalar(count_statement) or 0

    # 计算总页数
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 分页查询
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)

    # 执行分页查询语句，获取当前页的商品数据库模型列表
    # session.exec(statement) 执行构造好的SQL查询，返回结果集对象
    # .all() 将结果集转换为包含Product（数据库模型）实例的列表
    products = (await session.exec(statement)).all()

    # 将数据库模型列表转换为响应模型列表（核心：类型适配+数据校验）
    # 遍历每一个数据库查询得到的Product实例，逐个转换为对外输出的ProductResponse响应模型
    # model_validate：Pydantic v2核心方法，自动校验数据并完成模型转换，确保输出格式符合接口定义
    product_response = [
        ProductResponse.model_validate(product.model_dump()) for product in products
    ]

    return ProductListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        products=product_response,
    )


@router.get("/{product_id}", response_model=ProductResponse, summary="获取单个商品详情")
async def get_product(product_id: int, session: Session = Depends(get_session)):
    """根据ID获取商品详情"""
    statement = select(Product).where(Product.id == product_id)
    product = await session.exec(statement).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="创建新商品",
)
async def create_product(
    product_data: ProductCreateRequest, session: Session = Depends(get_session)
):
    """创建新商品"""
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        image_url=product_data.image_url,
        category=product_data.category,
        in_stock=product_data.in_stock,
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


@router.put("/{product_id}", response_model=ProductResponse, summary="更新商品信息")
async def update_product(
    product_id: int,
    product_data: ProductCreateRequest,
    session: Session = Depends(get_session),
):
    """更新商品信息"""
    statement = select(Product).where(Product.id == product_id)
    product = (await session.exec(statement)).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.image_url = product_data.image_url
    product.category = product_data.category
    product.in_stock = product_data.in_stock
    product.updated_at = datetime.now()

    session.add(product)
    await session.commit()
    await session.refresh(product)

    return product


@router.delete(
    "/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除商品"
)
async def delete_product(product_id: int, session: Session = Depends(get_session)):
    """删除商品"""
    statement = select(Product).where(Product.id == product_id)
    product = (await session.exec(statement)).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在")

    await session.delete(product)
    await session.commit()

    return None
