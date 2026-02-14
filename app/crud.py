from sqlalchemy.orm import Session
from app import models, schemas

def criar_funcionario(db: Session, funcionario: schemas.FuncionarioCreate):
    db_funcionario = models.Funcionario(**funcionario.dict())
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

def listar_funcionarios(db: Session):
    return db.query(models.Funcionario).all()

def buscar_funcionario(db: Session, funcionario_id: int):
    return db.query(models.Funcionario).filter(
        models.Funcionario.id == funcionario_id
    ).first()


def atualizar_funcionario(db: Session, funcionario_id: int, dados: schemas.FuncionarioCreate):
    funcionario = buscar_funcionario(db, funcionario_id)
    if funcionario:
        funcionario.nome = dados.nome
        funcionario.cargo = dados.cargo
        funcionario.salario = dados.salario
        db.commit()
        db.refresh(funcionario)
    return funcionario


def deletar_funcionario(db: Session, funcionario_id: int):
    funcionario = buscar_funcionario(db, funcionario_id)
    if funcionario:
        d
