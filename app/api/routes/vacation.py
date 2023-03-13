import time
from uuid import UUID
from typing import List, Optional
from fastapi import (
  APIRouter,
  Depends,
  HTTPException
)
import sqlalchemy as sa

from app.db.session import get_db
from app.schema.vacation import VacationSchema, VacationWithoutIdSchema
from app.repository.vacation import VacationRepository, VacationBadConflictError
from app.repository.balance import BalanceRepository

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  VacationRepository.delete_many(session)


@router.get("/", response_model=List[VacationSchema])
def get_vacations(session: sa.orm.Session = Depends(get_db)):
  return VacationRepository.get_many(session)


@router.get("/conflicts", response_model=List[VacationSchema])
def conflicts(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID, start_date: str, end_date: str):
  return VacationRepository.get_conflicts(session,
                                          employee_id=employee_id,
                                          start_date=start_date,
                                          end_date=end_date)


@router.post("/", response_model=Optional[VacationSchema])
def add_vacation(session: sa.orm.Session = Depends(get_db), *, vacation: VacationWithoutIdSchema):
  try:
    if vacation.start_date > vacation.end_date:
      raise HTTPException(status_code=400, detail="start_date must not be greated than end_date")
    
    if balance := BalanceRepository.get(session,
                                         employee_id=vacation.employee_id,
                                         vacation_type_id=vacation.vacation_type_id):
      delta = vacation.end_date - vacation.start_date
      if delta.days > balance.amount:
        raise HTTPException(status_code=400, detail="balance for vacation type is insufficient")

      balance.amount -= delta.days
      session.commit()

    vacation = VacationRepository.check_merge_conflicts(session, vacation)
    return VacationRepository.create(session, **vacation.dict())
  
  except VacationBadConflictError:
    raise HTTPException(status_code=400, detail="overlaps with another type of vacation")
  
  except sa.exc.IntegrityError:
    raise HTTPException(status_code=400, detail="unknown vacation type")


@router.post("/{vacation_id}", response_model=Optional[VacationSchema])
def update_vacation(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID, vacation_type_id: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
  if not (vacation := VacationRepository.get_by_id(session, vacation_id)):
    raise HTTPException(status_code=400, detail="unknown vacation")
  
  vacation_schema = VacationWithoutIdSchema(
    employee_id=vacation.employee_id,
    vacation_type_id=(vacation_type_id or vacation.vacation_type_id),
    start_date=start_date or str(vacation.start_date),
    end_date=end_date or str(vacation.end_date)
  )
  
  if vacation_schema.start_date > vacation_schema.end_date:
    raise HTTPException(status_code=400, detail="start_date must not be greater than end_date")

  try:
    current_delta = vacation.end_date - vacation.start_date
    
    vacation_schema = VacationRepository.check_merge_conflicts(session,
                                                              id_exceptions=[vacation.id],
                                                              vacation=vacation_schema)
    
    # update the balance if there is any, with the new delta
    if balance := BalanceRepository.get(session,
                                         employee_id=vacation.employee_id,
                                         vacation_type_id=vacation.vacation_type_id):
      new_delta = vacation_schema.end_date - vacation_schema.start_date
      if new_delta.days > balance.amount + current_delta.days:
        raise HTTPException(status_code=400, detail="balance for vacation type is insufficient")
      balance.amount -= new_delta.days - current_delta.days
    
    vacation.vacation_type_id = vacation_schema.vacation_type_id
    vacation.start_date = vacation_schema.start_date
    vacation.end_date = vacation_schema.end_date
    session.commit()
  except VacationBadConflictError:
    raise HTTPException(status_code=400, detail="overlaps with another type of vacation")
  except sa.exc.IntegrityError:
    raise HTTPException(status_code=400, detail="unknown vacation type")

  return vacation
  

@router.delete("/{vacation_id}", response_model=bool)
def delete_vacation(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID):
  if VacationRepository.delete(session, id=vacation_id) is None:
    raise HTTPException(status_code=400, detail="unknown vacation")
  return True


@router.get("/{vacation_id}", response_model=Optional[VacationSchema])
def get_vacations(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID):
  return VacationRepository.get_by_id(session, vacation_id)