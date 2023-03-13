from uuid import UUID

from .common import (
  client,
  TestClient,
  reset_databases,
  basic_employee
)

def test_add_employee_and_delete():
  reset_databases()
  
  employee1_res = basic_employee("A", "A")
  employee2_res = basic_employee("B", "B")
  
  assert employee1_res.status_code == 200
  assert employee2_res.status_code == 200
  
  employees_res = client.get("/employee")
  assert employees_res.status_code == 200
  employees_json = employees_res.json()
  
  assert len(employees_json) == 2
  assert employees_json[0]["first_name"] == "A"
  assert employees_json[0]["last_name"] == "A"
  assert employees_json[1]["first_name"] == "B"
  assert employees_json[1]["last_name"] == "B"
  
  employee1_res = client.delete(f"/employee/{employees_json[0]['id']}")
  assert employee1_res.status_code == 200
  
  employees_res = client.get("/employee")
  assert employees_res.status_code == 200
  employees_json = employees_res.json()
  
  assert len(employees_json) == 1
  