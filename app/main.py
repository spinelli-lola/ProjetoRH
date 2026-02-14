from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models import Funcionario
import app.schemas as schemas
import app.crud as crud
from fastapi import HTTPException


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/funcionarios", response_model=schemas.FuncionarioResponse)
def criar(funcionario: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    return crud.criar_funcionario(db, funcionario)

@app.get("/funcionarios", response_model=list[schemas.FuncionarioResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_funcionarios(db)

@app.get("/funcionarios/{funcionario_id}", response_model=schemas.FuncionarioResponse)
def buscar(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = crud.buscar_funcionario(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@app.put("/funcionarios/{funcionario_id}", response_model=schemas.FuncionarioResponse)
def atualizar(funcionario_id: int, dados: schemas.FuncionarioCreate, db: Session = Depends(get_db)):
    funcionario = crud.atualizar_funcionario(db, funcionario_id, dados)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@app.delete("/funcionarios/{funcionario_id}")
def deletar(funcionario_id: int, db: Session = Depends(get_db)):
    funcionario = crud.deletar_funcionario(db, funcionario_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"message": "Funcionário deletado com sucesso"}
