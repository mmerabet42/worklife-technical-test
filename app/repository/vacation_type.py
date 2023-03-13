from uuid import UUID

from app.model.vacation_type import VacationTypeModel
from .base import BaseRepository

class _VacationTypeRepository(BaseRepository):
  pass
  
VacationTypeRepository = _VacationTypeRepository(model=VacationTypeModel)