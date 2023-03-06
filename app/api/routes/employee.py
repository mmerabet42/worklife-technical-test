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
from app.repository.vacation import VacationRepository
from app.schema.employee import EmployeeSchema, EmployeeWithoutIdSchema
from app.schema.vacation import VacationSchema
from app.model.employee import EmployeeModel

router = APIRouter()

@router.post("/clear")
def clear(session: sa.orm.Session = Depends(get_db)):
  EmployeeRepository.delete_many(session)


@router.get("/", response_model=List[EmployeeSchema])
def get_employees(session: sa.orm.Session = Depends(get_db)):
  return EmployeeRepository.get_many(session)


@router.get("/{employee_id}", response_model=Optional[EmployeeSchema])
def get_employee(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID):
  return EmployeeRepository.get(session, id=employee_id)


@router.post("/add", response_model=Optional[EmployeeSchema])
def add_employee(session: sa.orm.Session = Depends(get_db), *, employee: EmployeeWithoutIdSchema):
  return EmployeeRepository.create(session, first_name=employee.first_name, last_name=employee.last_name)


@router.post("/delete/{employee_id}", response_model=bool)
def delete_employee(session: sa.orm.Session = Depends(get_db), *, employee_id: UUID):
  if EmployeeRepository.delete(session, id=employee_id) is None:
    raise HTTPException(status_code=400, detail="unknown employee")
  return True
