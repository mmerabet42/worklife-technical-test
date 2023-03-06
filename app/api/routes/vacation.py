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
from app.model.vacation import VacationModel
from app.schema.vacation import VacationSchema, VacationWithoutIdSchema
from app.repository.vacation import VacationRepository

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  VacationRepository.delete_many(session)


@router.get("/", response_model=List[VacationSchema])
def get_vacations(session: sa.orm.Session = Depends(get_db), *, employee_id: Optional[UUID] = None):
  if (employee_id is None):
    return VacationRepository.get_many(session)
  return VacationRepository.get_many(session, employee_id=employee_id)


@router.get("/conflicts", response_model=List[VacationSchema])
def conflicts(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID, start_date: str, end_date: str):
  return VacationRepository.get_conflicts(session,
                                          employee_id=employee_id,
                                          start_date=start_date,
                                          end_date=end_date)


@router.post("/add", response_model=Optional[VacationSchema])
def add_vacation(session: sa.orm.Session = Depends(get_db), *, vacation: VacationWithoutIdSchema):
  vacation = VacationRepository.check_merge_conflicts(session, vacation)
  return VacationRepository.create(session, **vacation.dict())


@router.post("/update/{vacation_id}", response_model=Optional[VacationSchema])
def update_vacation(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID, vacation_type: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
  if not (vacation := VacationRepository.get_by_id(session, vacation_id)):
    raise HTTPException(status_code=400, detail="unknown vacation")

  vacation_schema = VacationRepository.check_merge_conflicts(session,
                                                             id_exceptions=[vacation.id],
                                                             vacation=VacationWithoutIdSchema(
                                                               employee_id=vacation.employee_id,
                                                               vacation_type=(vacation_type or vacation.vacation_type),
                                                               start_date=start_date or str(vacation.start_date),
                                                               end_date=end_date or str(vacation.end_date)
                                                             ))

  vacation.vacation_type = vacation_schema.vacation_type
  vacation.start_date = vacation_schema.start_date
  vacation.end_date = vacation_schema.end_date
  session.commit()
  return vacation
  

@router.post("/delete/{vacation_id}", response_model=bool)
def delete_vacation(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID):
  if VacationRepository.delete(session, id=vacation_id) is None:
    raise HTTPException(status_code=400, detail="unknown vacation")
  return True


@router.get("/{vacation_id}", response_model=Optional[VacationSchema])
def get_vacations(session: sa.orm.Session = Depends(get_db), *, vacation_id: UUID):
  return VacationRepository.get_by_id(session, vacation_id)