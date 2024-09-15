from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database, bot_service

app = FastAPI()

# Database Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Endpoints
@app.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.email)
    if db_user and db_user.password == user.password:  # Simple password check
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")

@app.post("/search/")
def search_job(query: schemas.JobSearchQuery, db: Session = Depends(get_db)):
    bot_service.launch_bot_search(query, db)
    return {"message": "Bot search launched successfully"}
