from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, Base, SessionLocal
from app import crud, schemas, models

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Operação RH")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def adicionar_coluna_telefone_se_necessario():
    inspector = inspect(engine)
    if "candidatos" not in inspector.get_table_names():
        return

    colunas = [coluna["name"] for coluna in inspector.get_columns("candidatos")]
    if "telefone" not in colunas:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE candidatos ADD COLUMN telefone VARCHAR(20) NULL"))


def criar_dados_iniciais():
    db = SessionLocal()
    try:
        status_padrao = {
            1: "Novo",
            2: "Em Análise",
            3: "Aprovado",
            4: "Reprovado",
            5: "Excluído",
        }

        for status_id, nome in status_padrao.items():
            status = db.query(models.StatusProcesso).filter(models.StatusProcesso.id == status_id).first()
            if status:
                status.nome = nome
            else:
                db.add(models.StatusProcesso(id=status_id, nome=nome))

        funcionario = db.query(models.Funcionario).filter(models.Funcionario.id == 1).first()
        if not funcionario:
            db.add(models.Funcionario(
                id=1,
                nome="Responsável RH",
                cargo="Analista de RH",
                salario=3000.00,
                status_id=1,
            ))

        vaga = db.query(models.Vaga).filter(models.Vaga.id == 1).first()
        if not vaga:
            db.add(models.Vaga(
                id=1,
                titulo="Vaga Padrão",
                descricao="Vaga usada para cadastro rápido no Kanban",
                funcionario_id=1,
            ))

        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    adicionar_coluna_telefone_se_necessario()
    criar_dados_iniciais()


@app.get("/", include_in_schema=False)
def abrir_kanban():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/funcionarios", response_model=schemas.FuncionarioResponse)
def criar_funcionario(funcionario: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    return crud.criar_funcionario(db, funcionario)


@app.get("/funcionarios", response_model=list[schemas.FuncionarioResponse])
def listar_funcionarios(db: Session = Depends(get_db)):
    return crud.listar_funcionarios(db)


@app.get("/funcionarios/{id}", response_model=schemas.FuncionarioResponse)
def buscar_funcionario(id: int, db: Session = Depends(get_db)):
    funcionario = crud.buscar_funcionario(db, id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@app.put("/funcionarios/{id}", response_model=schemas.FuncionarioResponse)
def atualizar_funcionario(id: int, dados: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    funcionario = crud.atualizar_funcionario(db, id, dados)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@app.delete("/funcionarios/{id}")
def deletar_funcionario(id: int, db: Session = Depends(get_db)):
    funcionario = crud.deletar_funcionario(db, id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"message": "Funcionário removido com sucesso"}


@app.post("/candidatos", response_model=schemas.CandidatoResponse)
def criar_candidato(candidato: schemas.CandidatoCreate, db: Session = Depends(get_db)):
    if crud.buscar_candidato_por_email(db, candidato.email):
        raise HTTPException(status_code=400, detail="Já existe um candidato com este e-mail")

    if not crud.buscar_vaga(db, candidato.vaga_id):
        raise HTTPException(status_code=400, detail="Vaga não encontrada")

    if candidato.status_id not in [1, 2, 3, 4, 5]:
        raise HTTPException(status_code=400, detail="Status inválido")

    try:
        return crud.criar_candidato(db, candidato)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Não foi possível criar o candidato")


@app.get("/candidatos", response_model=list[schemas.CandidatoResponse])
def listar_candidatos(db: Session = Depends(get_db)):
    return crud.listar_candidatos(db)


@app.put("/candidatos/{id}/status", response_model=schemas.CandidatoResponse)
def atualizar_status_candidato(id: int, status_id: int, db: Session = Depends(get_db)):
    if status_id not in [1, 2, 3, 4, 5]:
        raise HTTPException(status_code=400, detail="Status inválido")

    candidato = crud.atualizar_candidato(db, id, status_id)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato


@app.post("/vagas", response_model=schemas.VagaResponse)
def criar_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    return crud.criar_vaga(db, vaga)


@app.get("/vagas", response_model=list[schemas.VagaResponse])
def listar_vagas(db: Session = Depends(get_db)):
    return crud.listar_vagas(db)


@app.post("/status", response_model=schemas.StatusResponse)
def criar_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    return crud.criar_status(db, status)


@app.get("/status", response_model=list[schemas.StatusResponse])
def listar_status(db: Session = Depends(get_db)):
    return crud.listar_status(db)
