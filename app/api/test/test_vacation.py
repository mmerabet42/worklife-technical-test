from uuid import UUID
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def clear_databases():
  client.post("/vacation/clear")
  client.post("/employee/clear")

def add_vacation(client: TestClient, employee_id: UUID, vacation_type: str, start_date: str, end_date: str):
  return client.post("/vacation/add", json={
    "employee_id": employee_id,
    "vacation_type": vacation_type,
    "start_date": start_date,
    "end_date": end_date
  })


def test_add_vacation_with_conflicts():
  clear_databases()
  employee_res = client.post("/employee/add", json={
    "first_name": "A",
    "last_name": "B"
  })
  employee_json = employee_res.json()
  
  assert add_vacation(client, employee_json["id"], "paid_leave", "2023-03-01", "2023-03-06").status_code == 200
  assert add_vacation(client, employee_json["id"], "paid_leave", "2023-03-08", "2023-03-11").status_code == 200
  assert add_vacation(client, employee_json["id"], "paid_leave", "2023-03-09", "2023-03-23").status_code == 200

  vacation_res = add_vacation(client, employee_json["id"], "paid_leave", "2023-03-03", "2023-03-20")
  assert vacation_res.status_code == 200
  assert vacation_res.json()["employee_id"] == employee_json["id"]
  assert vacation_res.json()["start_date"] == "2023-03-01"
  assert vacation_res.json()["end_date"] == "2023-03-23"
  
  all_vacations = client.get("/vacation")
  assert all_vacations.status_code == 200
  
  vacations_json = all_vacations.json()
  assert len(vacations_json) == 1
  assert vacations_json[0]["employee_id"] == employee_json["id"]
  assert vacations_json[0]["start_date"] == "2023-03-01"
  assert vacations_json[0]["end_date"] == "2023-03-23"


def test_update_vacation_with_conflicts_to_end():
  clear_databases()
  employee_res = client.post("/employee/add", json={
    "first_name": "A",
    "last_name": "B"
  })
  employee_json = employee_res.json()
  
  vac_to_update = add_vacation(client, employee_json["id"], "paid_leave", "2023-03-01", "2023-03-06")
  vac_to_update_json = vac_to_update.json()
  add_vacation(client, employee_json["id"], "paid_leave", "2023-03-08", "2023-03-11")

  vacation_res = client.post(f"/vacation/update/{vac_to_update_json['id']}?end_date=2023-03-10")
  assert vacation_res.status_code == 200
  assert vacation_res.json()["employee_id"] == employee_json["id"]
  assert vacation_res.json()["start_date"] == "2023-03-01"
  assert vacation_res.json()["end_date"] == "2023-03-11"
  
  all_vacations = client.get("/vacation")
  assert all_vacations.status_code == 200

  vacations_json = all_vacations.json()
  assert len(vacations_json) == 1
  assert vacations_json[0]["employee_id"] == employee_json["id"]
  assert vacations_json[0]["start_date"] == "2023-03-01"
  assert vacations_json[0]["end_date"] == "2023-03-11"
  
  
def test_update_vacation_with_conflicts_to_start():
  clear_databases()
  employee_res = client.post("/employee/add", json={
    "first_name": "A",
    "last_name": "B"
  })
  employee_json = employee_res.json()
  
  vac_to_update = add_vacation(client, employee_json["id"], "paid_leave", "2023-03-01", "2023-03-06")
  vac_to_update_json = vac_to_update.json()
  add_vacation(client, employee_json["id"], "paid_leave", "2023-02-10", "2023-02-25")

  vacation_res = client.post(f"/vacation/update/{vac_to_update_json['id']}?start_date=2023-02-20")
  assert vacation_res.status_code == 200
  assert vacation_res.json()["employee_id"] == employee_json["id"]
  assert vacation_res.json()["start_date"] == "2023-02-10"
  assert vacation_res.json()["end_date"] == "2023-03-06"
  
  all_vacations = client.get("/vacation")
  assert all_vacations.status_code == 200

  vacations_json = all_vacations.json()
  assert len(vacations_json) == 1
  assert vacations_json[0]["employee_id"] == employee_json["id"]
  assert vacations_json[0]["start_date"] == "2023-02-10"
  assert vacations_json[0]["end_date"] == "2023-03-06"
  

def test_overlaps_different_types():
  clear_databases()
  employee_res = client.post("/employee/add", json={
    "first_name": "A",
    "last_name": "B"
  })
  employee_json = employee_res.json()
  
  add_vacation(client, employee_json["id"], "unpaid_leave", "2023-03-01", "2023-03-06")
  assert add_vacation(client, employee_json["id"], "paid_leave", "2023-03-02", "2023-03-05").status_code == 400