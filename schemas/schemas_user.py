from pydantic import BaseModel

class User_Ia_Create(BaseModel):
    name: str
    sexo: str
    faixa_etaria: str
    idade: int
    raca_cor: str
    grupo: str
    renda: float
    estado: str
    escolaridade: str
    endereco: str
    numero: str
    bairro: str
    cidade: str
    UF: str
    CEP: str
    numero_moradores: int


class User_Ia(BaseModel):
    id: int
    name: str
    sexo: str
    faixa_etaria: str
    idade: int
    raca_cor: str
    grupo: str
    renda: float
    estado: str
    escolaridade: str
    endereco: str
    numero: str
    bairro: str
    cidade: str
    UF: str
    CEP: str
    numero_moradores: int
    classification: int

class Config:
    orm_mode = True