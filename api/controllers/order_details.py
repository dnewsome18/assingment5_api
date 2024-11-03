from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models.schemas import OrderDetail, OrderDetailCreate, OrderDetailUpdate

router = APIRouter()

@router.post("/order-details/", response_model=OrderDetail)
def create_order_detail(order_detail: OrderDetailCreate, db: Session = Depends(get_db)):
    new_order_detail = OrderDetail(**order_detail.dict())
    db.add(new_order_detail)
    db.commit()
    db.refresh(new_order_detail)
    return new_order_detail

@router.get("/order-details/", response_model=list[OrderDetail])
def read_all_order_details(db: Session = Depends(get_db)):
    order_details = db.query(OrderDetail).all()
    return order_details

@router.get("/order-details/{order_detail_id}", response_model=OrderDetail)
def read_one_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return order_detail

@router.put("/order-details/{order_detail_id}", response_model=OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: OrderDetailUpdate, db: Session = Depends(get_db)):
    existing_order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if existing_order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")

    for key, value in order_detail.dict(exclude_unset=True).items():
        setattr(existing_order_detail, key, value)

    db.commit()
    db.refresh(existing_order_detail)
    return existing_order_detail

@router.delete("/order-details/{order_detail_id}", response_model=dict)
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    order_detail = db.query(OrderDetail).filter(OrderDetail.id == order_detail_id).first()
    if order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")

    db.delete(order_detail)
    db.commit()
    return {"detail": "Order detail deleted"}