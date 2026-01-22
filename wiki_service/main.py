from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://wikiadmin:wikipass@postgres:5432/wikidb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

user_creation_counter = Counter('users_created_total', 'Total users created')
post_creation_counter = Counter('posts_created_total', 'Total posts created')

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserCreate(BaseModel):
    username: str
    email: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wiki Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Wiki Service API"}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_creation_counter.inc()
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    post_creation_counter.inc()
    return {"id": db_post.id, "title": db_post.title}

@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    return {"status": "healthy"}