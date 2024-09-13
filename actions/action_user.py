import pandas as pd
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from io import StringIO
from data_processor import classify_user, classify_user_from_csv
from models import userModel
from models.userModel import UserDataModel
from schemas import schemas_user


def get_user(db: Session, user_id: int):
  return db.query(userModel.UserDataModel).filter(userModel.UserDataModel.id == user_id).first()

def get_users_by_name(db: Session, name: str):
    try:
        users = db.query(UserDataModel).filter(UserDataModel.name == name).all()

        if not users:
            return {"detail": "Nenhum usuário encontrado com esse nome"}

        users_list = []
        for user in users:
            user_dict = user.__dict__
            user_dict.pop('_sa_instance_state', None)
            users_list.append(user_dict)

        return users_list
    except Exception as e:
        return {"detail": str(e)}

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(userModel.UserDataModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas_user.User_Ia_Create):
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

def delete_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(UserDataModel).filter(UserDataModel.id == user_id).one_or_none()

        if not user:
            return {"detail": "Usuário não encontrado"}

        db.delete(user)
        db.commit()

        return {"detail": "Usuário deletado com sucesso"}
    except Exception as e:
        db.rollback()
        return {"detail": str(e)}

def get_recent_users(db: Session, limit: int = 10):
    try:
        # Busca os usuários ordenados pelo ID em ordem decrescente (últimos registros primeiro)
        users = db.query(UserDataModel).order_by(UserDataModel.id.desc()).limit(limit).all()

        if not users:
            return {"detail": "Nenhum usuário encontrado"}

        # Converte os resultados para uma lista de dicionários, se necessário
        user_list = [user.__dict__ for user in users]

        # Remove o campo '_sa_instance_state' que é adicionado automaticamente pelo SQLAlchemy
        for user in user_list:
            user.pop('_sa_instance_state', None)

        return user_list
    except Exception as e:
        return {"detail": str(e)}


def get_users_by_classification_paginated(db: Session, is_vulnerable: bool, page: int = 1, page_size: int = 10):
    try:
        classification_value = 1 if is_vulnerable else 0

        skip = (page - 1) * page_size

        users = (
            db.query(UserDataModel)
            .filter(UserDataModel.classification == classification_value)
            .offset(skip)
            .limit(page_size)
            .all()
        )

        if not users:
            return {"detail": "Nenhum usuário encontrado com o status de vulnerabilidade especificado"}

        user_list = jsonable_encoder(users)

        return user_list
    except Exception as e:
        return {"detail": str(e)}

class UserAction:

    def __init__(self, db: Session):
        self.db = db

    def classify_and_save_csv(self, db: Session, file: UploadFile):
        if file.content_type != 'text/csv':
            raise ValueError("Invalid file format. Please upload a CSV file.")

        content = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(content))

        classification_result = classify_user_from_csv(df)
        df['classification'] = classification_result

        for index, row in df.iterrows():
            try:
                idade = int(row['idade']) if not pd.isna(row['idade']) else None
                renda = float(row['renda']) if not pd.isna(row['renda']) else None
                numero_moradores = int(row['n_moradores']) if not pd.isna(row['n_moradores']) else None
                classification = int(row['classification']) if not pd.isna(row['classification']) else None

                user_data = UserDataModel(
                    name=row['nome'],
                    sexo=row['sexo'],
                    faixa_etaria=row['faixa_etaria'],
                    idade=idade,
                    raca_cor=row['raca_cor'],
                    grupo=row['grupo'],
                    renda=renda,
                    estado=row['estado'],
                    escolaridade=row['escolaridade'],
                    endereco=row['endereco'],
                    numero=row['numero'],
                    bairro=row['bairro'],
                    cidade=row['cidade'],
                    UF=row['UF'],
                    CEP=row['CEP'],
                    numero_moradores=numero_moradores,
                    classification=classification
                )

                self.db.add(user_data)
            except Exception as e:
                print(f"Error at index {index}: {e}")
                print(f"Row data: {row}")

        db.commit()

        vulneraveis = df['classification'].sum()
        nao_vulneraveis = len(df) - vulneraveis

        return {"vulneraveis": int(vulneraveis), "nao_vulneraveis": int(nao_vulneraveis)}


