from sqlalchemy.orm import Session

from passlib.context import CryptContext

from schemas import schemas
from models import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
  return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = get_password_hash(user.password)
  db_user = models.User(
    email=user.email,
    hashed_password=hashed_password,
    name=user.name
  )
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
  user = db.query(models.User).filter(models.User.email == email).first()
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user