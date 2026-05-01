from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


#  FUNCIONÁRIOS

class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    salario = Column(Float, nullable=False)
    status_id = Column(Integer, nullable=False, default=1) # 1 Novo - 2 Em análise - 3 Aprovado

    vagas = relationship("Vaga", back_populates="responsavel")


#  STATUS PROCESSO SELETIVO

class StatusProcesso(Base):
    __tablename__ = "status_processo"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)

    candidatos = relationship("Candidato", back_populates="status")


#  VAGAS

class Vaga(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255))

    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))

    responsavel = relationship("Funcionario", back_populates="vagas")
    candidatos = relationship("Candidato", back_populates="vaga")


#  CANDIDATOS

class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    vaga_id = Column(Integer, ForeignKey("vagas.id"))
    status_id = Column(Integer, ForeignKey("status_processo.id"))

    vaga = relationship("Vaga", back_populates="candidatos")
    status = relationship("StatusProcesso", back_populates="candidatos")