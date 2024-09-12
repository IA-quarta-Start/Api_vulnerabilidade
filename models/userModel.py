from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Index

from connection.connection import Base

class UserDataModel(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    name= Column(String)
    sexo= Column(String)
    faixa_etaria= Column(String)
    idade= Column(Numeric)
    raca_cor= Column(String)
    grupo= Column(String)
    renda= Column(Numeric)
    estado= Column(String)
    escolaridade= Column(String)
    endereco= Column(String)
    numero= Column(String)
    bairro= Column(String)
    cidade= Column(String)
    UF= Column(String)
    CEP= Column(String)
    numero_moradores= Column(Numeric)
    classification = Column(Integer, nullable=True)

    # Definir o índice na coluna classification
    __table_args__ = (
        Index('idx_classification', 'classification'),
    )