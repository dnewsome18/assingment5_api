from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models.schemas import Resource, ResourceCreate, ResourceUpdate

router = APIRouter()

@router.post("/resources/", response_model=Resource)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    new_resource = Resource(**resource.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

@router.get("/resources/", response_model=list[Resource])
def read_all_resources(db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources

@router.get("/resources/{resource_id}", response_model=Resource)
def read_one_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)):
    existing_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if existing_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    for key, value in resource.dict(exclude_unset=True).items():
        setattr(existing_resource, key, value)

    db.commit()
    db.refresh(existing_resource)
    return existing_resource

@router.delete("/resources/{resource_id}", response_model=dict)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(resource)
    db.commit()
    return {"detail": "Resource deleted"}