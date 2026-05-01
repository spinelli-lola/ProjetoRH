from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import crud, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CRIA AS TABELAS AO INICIAR
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# DEPENDÊNCIA DO BANCO
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    return crud.criar_candidato(db, candidato)

@app.get("/candidatos", response_model=list[schemas.CandidatoResponse])
def listar_candidatos(db: Session = Depends(get_db)):
    return crud.listar_candidatos(db)

@app.put("/candidatos/{id}/status", response_model=schemas.CandidatoResponse)
def atualizar_status_candidato(id: int, status_id: int, db: Session = Depends(get_db)):
    candidato = crud.atualizar_candidato(db, id, status_id)
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")
    return candidato

#  VAGAS

@app.post("/vagas", response_model=schemas.VagaResponse)
def criar_vaga(vaga: schemas.VagaCreate, db: Session = Depends(get_db)):
    return crud.criar_vaga(db, vaga)

@app.get("/vagas", response_model=list[schemas.VagaResponse])
def listar_vagas(db: Session = Depends(get_db)):
    return crud.listar_vagas(db)

#  STATUS DO PROCESSO 

@app.post("/status", response_model=schemas.StatusResponse)
def criar_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    return crud.criar_status(db, status)

@app.get("/status", response_model=list[schemas.StatusResponse])
def listar_status(db: Session = Depends(get_db)):
    return crud.listar_status(db)