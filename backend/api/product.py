"""
商品管理API路由
功能：提供商品的增删改查接口，支持分页查询
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from datetime import datetime
import math

from model.product import Product
from schemas.product import ProductResponse, ProductListResponse, ProductCreateRequest
from database import get_session

router = APIRouter(prefix="/api", tags=["products"])


@router.get(
    "/products",
    response_model=ProductListResponse,
    summary="获取商品列表（分页）接口",
    description="获取所有商品列表，支持分页查询",
)
async def get_products(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量，最大100"),
    category: str = Query(None, description="商品分类筛选"),
    session: Session = Depends(get_session),
):
    """获取商品列表（带分页）"""
    # 构建查询语句
    statement = select(Product)

    # 如果有分类筛选
    if category:
        statement = statement.where(Product.category == category)

    # 只显示有库存的商品
    statement = statement.where(Product.in_stock == True)

    # 按创建时间倒序排列
    statement = statement.order_by(Product.created_at.desc())

    # 获取总数
    count_statement = select(func.count(Product))
    if category:
        count_statement = count_statement.where(Product.category == category)
    count_statement = count_statement.where(Product.in_stock == True)

    total = await session.scalar(count_statement) or 0

    # 计算总页数
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    # 分页查询
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size)

    products = (await session.exec(statement)).all()

    return ProductListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        products=products,
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
