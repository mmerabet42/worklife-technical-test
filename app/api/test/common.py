from uuid import UUID
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def reset_databases():
  client.delete("/clear_all")
  
def basic_employee(first_name = "A", last_name = "A"):
  return client.post("/employee", json={
    "first_name": first_name,
    "last_name": last_name
  })
  
def basic_vacation_type(name = "paid_leave"):
  return client.post("/vacation_type", json={
    "name": name
  })
  
def check_and_json(http_query, status_code = 200) -> tuple:
  assert http_query.status_code == status_code
  return (http_query, http_query.json())

def basic_vacation(employee_id: UUID, vacation_type_id: UUID, start_date: str, end_date: str):
  return client.post("/vacation", json={
    "employee_id": employee_id,
    "vacation_type_id": vacation_type_id,
    "start_date": start_date,
    "end_date": end_date
  })