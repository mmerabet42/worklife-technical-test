from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
  pass

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
