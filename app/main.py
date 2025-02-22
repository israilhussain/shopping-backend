# app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Shopping API"}

app.include_router(router)