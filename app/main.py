from fastapi import FastAPI, Depends
import sqlalchemy as sa
import types

from app.api import add_app_routes
from app.core.config import settings
from app.db.session import get_db
import app.repository as repositories


app = FastAPI(
  title=settings.PROJECT_NAME,
  version=settings.VERSION,
)

@app.delete("/clear_all")
def clear_all(session: sa.orm.Session = Depends(get_db)):
  # Basically we're just iterating through each repositories and performing a delete_many for each
  for _, c in repositories.__dict__.items():
    if isinstance(c, types.ModuleType):
      for name, c in c.__dict__.items():
        if not name.startswith('_') and name.endswith('Repository') and name != "BaseRepository":
          c.delete_many(session)

add_app_routes(app)
