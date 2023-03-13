from uuid import UUID

from app.model.balance import BalanceModel
from .base import BaseRepository

class _BalanceRepository(BaseRepository):
  pass
  
BalanceRepository = _BalanceRepository(model=BalanceModel)