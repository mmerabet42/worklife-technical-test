from uuid import UUID

from .common import (
  client,
  TestClient,
  reset_databases,
  basic_employee,
  basic_vacation_type,
  basic_vacation,
  check_and_json
)

def test_add_vacation_then_delete():
  reset_databases()
  _, employee_json = check_and_json(basic_employee("A", "B"))
  paid_leave_json = basic_vacation_type("paid_leave").json()
  
  vacation_res = basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-01", "2023-03-06")
  assert vacation_res.status_code == 200
  
  all_vacations_res = client.get("/vacation")
  assert all_vacations_res.status_code == 200
  
  vacations_json = all_vacations_res.json()
  assert len(vacations_json) == 1
  assert vacations_json[0]["id"] == vacation_res.json()["id"]
  assert vacations_json[0]["employee_id"] == employee_json["id"]
  assert vacations_json[0]["start_date"] == "2023-03-01"
  assert vacations_json[0]["end_date"] == "2023-03-06"
  
  assert client.delete(f"/vacation/{vacations_json[0]['id']}").status_code == 200
  
  all_vacations_res = client.get("/vacation")
  assert all_vacations_res.status_code == 200
  
  vacations_json = all_vacations_res.json()
  assert len(vacations_json) == 0


def test_vacation_with_start_date_greater():
  reset_databases()
  
  _, employee_json = check_and_json(basic_employee("A", "B"))
  _, paid_leave_json = check_and_json(basic_vacation_type("paid_leave"))
  
  check_and_json(basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-20", "2023-03-15"), 400)
  
  _, vac_json = check_and_json(basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-10", "2023-03-12"))
  check_and_json(client.post(f"/vacation/{vac_json['id']}?start_date=2023-03-20"), 400)

def test_add_vacation_with_conflicts_of_same_type():
  reset_databases()
  employee_json = basic_employee("A", "B").json()
  paid_leave_json = basic_vacation_type("paid_leave").json()
  
  assert basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-01", "2023-03-06").status_code == 200
  assert basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-08", "2023-03-11").status_code == 200
  assert basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-09", "2023-03-23").status_code == 200

  vacation_json = basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-03", "2023-03-20").json()
  assert vacation_json["employee_id"] == employee_json["id"]
  assert vacation_json["start_date"] == "2023-03-01"
  assert vacation_json["end_date"] == "2023-03-23"
  
  all_vacations = client.get("/vacation")
  assert all_vacations.status_code == 200
  
  vacations_json = all_vacations.json()
  assert len(vacations_json) == 1
  assert vacations_json[0]["employee_id"] == employee_json["id"]
  assert vacations_json[0]["start_date"] == "2023-03-01"
  assert vacations_json[0]["end_date"] == "2023-03-23"


def test_update_vacation_with_conflicts_of_same_type_1():
  reset_databases()
  employee_json = basic_employee("A", "B").json()
  paid_leave_json = basic_vacation_type("paid_leave").json()
  
  vac_to_update = basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-01", "2023-03-06")
  vac_to_update_json = vac_to_update.json()
  basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-08", "2023-03-11")

  vacation_res = client.post(f"/vacation/{vac_to_update_json['id']}?end_date=2023-03-10")
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
  
  
def test_update_vacation_with_conflicts_of_same_type_2():
  reset_databases()
  employee_json = basic_employee("A", "B").json()
  paid_leave_json = basic_vacation_type("paid_leave").json()
  
  vac_to_update = basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-01", "2023-03-06")
  vac_to_update_json = vac_to_update.json()
  basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-02-10", "2023-02-25")

  vacation_res = client.post(f"/vacation/{vac_to_update_json['id']}?start_date=2023-02-20")
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
  

def test_add_vacation_with_conflicts_of_different_type_must_be_cancelled():
  reset_databases()
  employee_json = basic_employee("A", "B").json()
  paid_leave_json = basic_vacation_type("paid_leave").json()
  unpaid_leave_json = basic_vacation_type("unpaid_leave").json()
  
  basic_vacation(employee_json["id"], unpaid_leave_json["id"], "2023-03-01", "2023-03-06")
  assert basic_vacation(employee_json["id"], paid_leave_json["id"], "2023-03-02", "2023-03-05").status_code == 400