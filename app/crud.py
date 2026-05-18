from sqlalchemy.orm import Session
from app import models, schemas


# FUNCIONÁRIOS

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
        db.delete(funcionario)
        db.commit()
        return funcionario
    return None


# STATUS PROCESSO

def criar_status(db: Session, status: schemas.StatusCreate):
    obj = models.StatusProcesso(**status.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def listar_status(db: Session):
    return db.query(models.StatusProcesso).all()


# VAGAS

def criar_vaga(db: Session, vaga: schemas.VagaCreate):
    obj = models.Vaga(**vaga.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def listar_vagas(db: Session):
    return db.query(models.Vaga).all()


def buscar_vaga(db: Session, vaga_id: int):
    return db.query(models.Vaga).filter(
        models.Vaga.id == vaga_id
    ).first()


# CANDIDATOS

def buscar_candidato_por_email(db: Session, email: str):
    return db.query(models.Candidato).filter(
        models.Candidato.email == email
    ).first()


def criar_candidato(db: Session, candidato: schemas.CandidatoCreate):
    obj = models.Candidato(**candidato.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def listar_candidatos(db: Session):
    return db.query(models.Candidato).order_by(models.Candidato.id.desc()).all()


def buscar_candidato(db: Session, candidato_id: int):
    return db.query(models.Candidato).filter(
        models.Candidato.id == candidato_id
    ).first()


def atualizar_candidato(db: Session, candidato_id: int, status_id: int):
    candidato = buscar_candidato(db, candidato_id)
    if candidato:
        candidato.status_id = status_id
        db.commit()
        db.refresh(candidato)
    return candidato


def deletar_candidato(db: Session, candidato_id: int):
    candidato = buscar_candidato(db, candidato_id)
    if candidato:
        db.delete(candidato)
        db.commit()
        return candidato
    return None
