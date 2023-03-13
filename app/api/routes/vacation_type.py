from uuid import UUID
from typing import Optional, List
from fastapi import (
  Depends,
  APIRouter,
  HTTPException
)

import sqlalchemy as sa

from app.db.session import get_db
from app.repository.vacation_type import VacationTypeRepository
from app.schema.vacation_type import (
  VacationTypeSchema,
  VacationTypeWithoutIdSchema,
  VacationTypeWithRelationshipSchema
) 

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  VacationTypeRepository.delete_many(session)


@router.get("/", response_model=List[VacationTypeSchema])
def all_vacation_type(session: sa.orm.Session = Depends(get_db)):
  return VacationTypeRepository.get_many(session)


@router.get("/{vacation_type_id}", response_model=Optional[VacationTypeWithRelationshipSchema])
def get_vacation_type(session: sa.orm.Session = Depends(get_db), *, vacation_type_id: UUID):
  return VacationTypeRepository.get_by_id(session, vacation_type_id)


@router.post("/", response_model=Optional[VacationTypeSchema])
def add_vacation_type(session: sa.orm.Session = Depends(get_db), *, vacation_type: VacationTypeWithoutIdSchema):
  return VacationTypeRepository.create(session, **vacation_type.dict())


@router.delete("/{vacation_type_id}", response_model=bool)
def add_vacation_type(session: sa.orm.Session = Depends(get_db), *, vacation_type_id: UUID):
  if VacationTypeRepository.delete(session, id=vacation_type_id) is None:
    raise HTTPException(status_code=400, detail="unknown vacation type")
  return True