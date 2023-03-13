from uuid import UUID
from typing import Optional, List
from fastapi import (
  Depends,
  APIRouter,
  HTTPException
)
import sqlalchemy as sa

from app.db.session import get_db
from app.repository.balance import BalanceRepository
from app.schema.balance import BalanceSchema, BalanceWithoutIdSchema

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  BalanceRepository.delete_many(session)
  
  
@router.get("/", response_model=List[BalanceSchema])
def all_balances(session: sa.orm.Session = Depends(get_db)):
  return BalanceRepository.get_many(session)


@router.get("/{balance_id}", response_model=Optional[BalanceSchema])
def get_balance(session: sa.orm.Session = Depends(get_db), *, balance_id: UUID):
  return BalanceRepository.get_by_id(session, balance_id)
  
  
@router.post("/", response_model=Optional[BalanceSchema])
def add_balance(session: sa.orm.Session = Depends(get_db), *, balance: BalanceWithoutIdSchema):
  try:
    return BalanceRepository.create(session, **balance.dict())
  except sa.exc.IntegriyError:
    raise HTTPException(status_code=400, detail="balance already exists")
  
  
@router.delete("/{balance_id}", response_model=bool)
def delete_balance(session: sa.orm.Session = Depends(get_db), *, balance_id: UUID):
  if BalanceRepository.delete(session, id=balance_id) is None:
    raise HTTPException(status_code=400, detail="unknown balance")
  return True