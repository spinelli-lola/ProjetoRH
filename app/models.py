from sqlalchemy import Column, Integer, String
from .database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    cargo = Column(String(100))
    salario = Column(Integer)
