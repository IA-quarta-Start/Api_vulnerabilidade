from sqlalchemy.orm import Session

from data_processor import classify_user
from models import userModel
from models.userModel import UserDataModel
from schemas import schemas_user


def get_user(db: Session, user_id: int):
  return db.query(userModel.UserDataModel).filter(userModel.UserDataModel.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(userModel.UserDataModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas_user.User_Ia_Create):
    # Classificar o usuário
    classification_result = classify_user(user)

    db_user= userModel.UserDataModel(
        name=user.name,
        sexo=user.sexo,
        faixa_etaria=user.faixa_etaria,
        idade=user.idade,
        raca_cor=user.raca_cor,
        grupo=user.grupo,
        renda=user.renda,
        estado=user.estado,
        escolaridade=user.escolaridade,
        endereco=user.endereco,
        numero=user.numero,
        bairro=user.bairro,
        cidade=user.cidade,
        UF=user.UF,
        CEP=user.CEP,
        numero_moradores=user.numero_moradores,
        classification=classification_result
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user