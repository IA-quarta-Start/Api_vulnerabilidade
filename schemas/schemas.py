from pydantic import BaseModel

class UserCreate(BaseModel):
    password: str
    email: str
    name: str

class Userlogin(BaseModel):
    password: str
    email: str

class User(BaseModel):
    id: int
    name: str
    is_active: bool

class Config:
    orm_mode = True