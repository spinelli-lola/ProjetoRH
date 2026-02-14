from pydantic import BaseModel

class FuncionarioBase(BaseModel):
    nome: str
    cargo: str
    salario: int

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioResponse(FuncionarioBase):
    id: int

    class Config:
        from_attributes = True
