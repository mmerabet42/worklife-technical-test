from fastapi import FastAPI

from .routes import (
  health,
  employee,
  vacation,
  vacation_type,
  balance
)


def add_app_routes(app: FastAPI):
  app.include_router(health.router, prefix="/health", tags=["Health"])
  app.include_router(employee.router, prefix="/employee", tags=["Employee"])
  app.include_router(vacation.router, prefix="/vacation", tags=["Vacation"])
  app.include_router(vacation_type.router, prefix="/vacation_type", tags=["Vacation Type"])
  app.include_router(balance.router, prefix="/balance", tags=["Balance"])
