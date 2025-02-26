from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Product
from app.utils import upload_image_to_s3

app = FastAPI()

Base.metadata.create_all(bind=engine)


origins = [
    "http://shopping.us-east-1.elasticbeanstalk.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/")
async def create_product(
    title: str,
    price: float,
    description: str,
    category: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_url = upload_image_to_s3(image)

    new_product = Product(
        title=title,
        price=price,
        description=description,
        category=category,
        image_url=image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "product": new_product}

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/")
async def root():
    return {"message": "API is healthy!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}