from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models.schemas import Recipe, RecipeCreate, RecipeUpdate

router = APIRouter()

@router.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

@router.get("/recipes/", response_model=list[Recipe])
def read_all_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).all()
    return recipes

@router.get("/recipes/{recipe_id}", response_model=Recipe)
def read_one_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
    existing_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if existing_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(existing_recipe, key, value)

    db.commit()
    db.refresh(existing_recipe)
    return existing_recipe

@router.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"detail": "Recipe deleted"}