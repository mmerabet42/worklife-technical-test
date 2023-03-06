from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
  def get_by_id(self, session, employee_id) -> EmployeeModel:
    return self.query(session, self.model.id == employee_id)

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
