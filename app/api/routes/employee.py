from typing import Optional, List
from uuid import UUID

from fastapi import (
  Depends,
  APIRouter,
  HTTPException
)
import sqlalchemy as sa

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema.employee import EmployeeSchema, EmployeeWithoutIdSchema, EmployeeWithRelationshipSchema

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  EmployeeRepository.delete_many(session)


@router.get("/", response_model=List[EmployeeSchema])
def get_employees(session: sa.orm.Session = Depends(get_db)):
  return EmployeeRepository.get_many(session)


@router.get("/{employee_id}", response_model=Optional[EmployeeWithRelationshipSchema])
def get_employee(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID):
  return EmployeeRepository.get_by_id(session, employee_id)


@router.post("/", response_model=Optional[EmployeeSchema])
def add_employee(session: sa.orm.Session = Depends(get_db), *, employee: EmployeeWithoutIdSchema):
  return EmployeeRepository.create(session, first_name=employee.first_name, last_name=employee.last_name)


@router.delete("/{employee_id}", response_model=bool)
def delete_employee(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID):
  if EmployeeRepository.delete(session, id=employee_id) is None:
    raise HTTPException(status_code=400, detail="unknown employee")
  return True
