from uuid import UUID
import sqlalchemy as sa
from fastapi import HTTPException
from typing import Optional

from app.model.vacation import VacationModel
from app.schema.vacation import VacationWithoutIdSchema
from .base import BaseRepository

class VacationBadConflictError(Exception):
  pass

class _VacationRepository(BaseRepository):
  # def get_by_id(self, session: sa.orm.Session, vacation_id: UUID) -> VacationModel:
  #   return self.query(session, self.model.id == vacation_id).one_or_none()
  
  def get_conflicts(self, session: sa.orm.Session, *, employee_id: UUID, start_date: str, end_date: str, id_exceptions: Optional[tuple[UUID]] = None) -> list[VacationModel]:
    id_exceptions = id_exceptions or ()
    
    return self.get_many(session,
                         sa.and_(
                           VacationModel.id.notin_(id_exceptions),
                           VacationModel.employee_id == employee_id,
                           sa.or_(
                             sa.and_(start_date >= VacationModel.start_date, start_date <= VacationModel.end_date),
                             sa.and_(end_date >= VacationModel.start_date, end_date <= VacationModel.end_date),
                             
                             sa.and_(start_date <= VacationModel.start_date, end_date >= VacationModel.end_date),
                             sa.and_(VacationModel.start_date <= start_date, VacationModel.end_date >= end_date),
                           )
                         ))

  def check_merge_conflicts(self, session: sa.orm.Session, vacation: VacationWithoutIdSchema, id_exceptions: Optional[tuple[UUID]] = None) -> VacationWithoutIdSchema:
    conflicts = VacationRepository.get_conflicts(session,
                                               id_exceptions=id_exceptions,
                                               employee_id=vacation.employee_id,
                                               start_date=vacation.start_date,
                                               end_date=vacation.end_date)
    if any(v.vacation_type_id != vacation.vacation_type_id for v in conflicts):
      raise VacationBadConflictError()
    
    # [print(f"Conflict: {c}") for c in conflicts]
    # return None
    
    if conflicts:
      # Getting the min and max boundaries of the conflicted vacations
      
      # i could have done this below, but i think it's better to do it in one single loop
      # min_start_date = min(conflicts, key=lambda v: v.start_date)
      # max_end_date = max(conflicts, key=lambda v: v.end_date)

      for v in conflicts:
        if v.start_date < vacation.start_date:
          vacation.start_date = v.start_date
        if v.end_date > vacation.end_date:
          vacation.end_date = v.end_date
      
      # delete all the conflicts
      vacation_ids = map(lambda v: v.id, conflicts)
      VacationRepository.delete_many(session, VacationModel.id.in_(vacation_ids))
    return vacation
  
VacationRepository = _VacationRepository(model=VacationModel)