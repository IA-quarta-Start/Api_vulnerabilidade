
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from actions.action_user import UserAction, \
    get_users_by_name, delete_user_by_id, get_users_by_classification_paginated

from schemas import schemas_user, schemas
from actions import action_user, actions
from models import models

from connection.connection import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Isso resolve os erros de Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir apenas essa origem
    allow_credentials=True,  # Permitir envio de cookies ou credenciais
    allow_methods=["*"],  # Permitir todos os métodos HTTP (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.get("/")
def read_root():
    return {"message": "CORS habilitado com sucesso!"}
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/admin/", response_model=schemas.User)
def create_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = actions.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return actions.create_user(db=db, user=user)

@app.get("/admin/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = actions.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/admin/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = actions.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas_user.User_Ia)
def create_user(user: schemas_user.User_Ia_Create, db: Session = Depends(get_db)):
    return action_user.create_user(db=db, user=user)


@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Instancia a classe UserAction e chama a função de classificação
        user_action = UserAction(db)
        result = user_action.classify_and_save_csv(db, file)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{name}")
def read_users(name: str, db: Session = Depends(get_db)):
    result = get_users_by_name(db, name)

    if isinstance(result, dict) and "detail" in result:
        raise HTTPException(status_code=404, detail=result["detail"])

    return result

@app.get("/users/", response_model=list[schemas_user.User_Ia])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = action_user.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/vulnerability/")
def filter_users_by_vulnerability(is_vulnerable: bool, page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    result = get_users_by_classification_paginated(db, is_vulnerable, page=page, page_size=page_size)

    if isinstance(result, dict) and "detail" in result:
        raise HTTPException(status_code=404, detail=result["detail"])

    return result


@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    result = delete_user_by_id(db, user_id)

    if isinstance(result, dict) and "detail" in result:
        raise HTTPException(status_code=404, detail=result["detail"])

    return result