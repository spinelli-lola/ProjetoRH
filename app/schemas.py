from pydantic import BaseModel
from typing import Optional


#  FUNCIONÁRIO 

class FuncionarioBase(BaseModel):
    nome: str
    cargo: str
    salario: float


class FuncionarioCreate(FuncionarioBase):
    pass


class FuncionarioResponse(FuncionarioBase):
    id: int

    class Config:
        orm_mode = True


#  STATUS PROCESSO 

class StatusBase(BaseModel):
    nome: str


class StatusCreate(StatusBase):
    pass


class StatusResponse(StatusBase):
    id: int

    class Config:
        orm_mode = True


#  VAGA

class VagaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    funcionario_id: int


class VagaCreate(VagaBase):
    pass


class VagaResponse(VagaBase):
    id: int

    class Config:
        orm_mode = True


#  CANDIDATO

class CandidatoBase(BaseModel):
    nome: str
    email: str
    vaga_id: int
    status_id: int


class CandidatoCreate(CandidatoBase):
    pass


class CandidatoResponse(CandidatoBase):
    id: int

    class Config:
        orm_mode = True