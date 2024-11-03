from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models.schemas import Sandwich
from api.models.schemas import SandwichCreate, SandwichUpdate

router = APIRouter()


@router.post("/sandwiches/", response_model=Sandwich)
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    new_sandwich = Sandwich(**sandwich.dict())
    db.add(new_sandwich)
    db.commit()
    db.refresh(new_sandwich)
    return new_sandwich


@router.get("/sandwiches/", response_model=list[Sandwich])
def read_all_sandwiches(db: Session = Depends(get_db)):
    sandwiches = db.query(Sandwich).all()
    return sandwiches


@router.get("/sandwiches/{sandwich_id}", response_model=Sandwich)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich


@router.put("/sandwiches/{sandwich_id}", response_model=Sandwich)
def update_sandwich(sandwich_id: int, sandwich: SandwichUpdate, db: Session = Depends(get_db)):
    existing_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if existing_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    for key, value in sandwich.dict(exclude_unset=True).items():
        setattr(existing_sandwich, key, value)

    db.commit()
    db.refresh(existing_sandwich)
    return existing_sandwich


@router.delete("/sandwiches/{sandwich_id}", response_model=dict)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    db.delete(sandwich)
    db.commit()
    return {"detail": "Sandwich deleted"}
