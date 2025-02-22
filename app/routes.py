# app/routes.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
def get_products():
    return [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]