"""
MedLinka — Orders Router
POST /api/v1/orders           — place order
GET  /api/v1/orders           — patient's orders
GET  /api/v1/orders/{id}      — single order
DELETE /api/v1/orders/{id}    — cancel order
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User, Order, OrderItem, Medicine, OrderStatus, UserRole
from app.schemas.schemas import OrderCreate, OrderOut, OKResponse
from app.utils.dependencies import get_current_user, require_role
from app.i18n import t, get_language_from_header

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def place_order(
    body: OrderCreate,
    current_user: User = Depends(require_role(UserRole.PATIENT)),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    total = 0.0
    items_to_create = []

    for item in body.items:
        med_result = await db.execute(select(Medicine).where(Medicine.id == item.medicine_id))
        med = med_result.scalar_one_or_none()

        if not med or not med.is_active:
            raise HTTPException(status_code=404, detail=t("medicine.not_found", lang))
        if med.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=t("medicine.out_of_stock", lang))

        total += med.price * item.quantity
        items_to_create.append((item, med))

    order = Order(
        patient_id=current_user.id,
        total_price=round(total, 2),
        delivery_address=body.delivery_address,
        notes=body.notes,
    )
    db.add(order)
    await db.flush()

    for item, med in items_to_create:
        db.add(OrderItem(
            order_id=order.id,
            medicine_id=item.medicine_id,
            quantity=item.quantity,
            unit_price=med.price,
        ))
        med.stock_quantity -= item.quantity

    await db.commit()
    await db.refresh(order)
    return order


@router.get("", response_model=List[OrderOut])
async def list_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Order).where(Order.patient_id == current_user.id).order_by(Order.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail=t("order.not_found", lang))
    return order


@router.delete("/{order_id}", response_model=OKResponse)
async def cancel_order(
    order_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    accept_language: Optional[str] = Header(default=None),
):
    lang = get_language_from_header(accept_language)
    result = await db.execute(select(Order).where(Order.id == order_id, Order.patient_id == current_user.id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail=t("order.not_found", lang))
    if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
        raise HTTPException(status_code=400, detail=t("order.already_shipped", lang))

    order.status = OrderStatus.CANCELLED
    await db.commit()
    return OKResponse(message=t("order.cancelled", lang))
