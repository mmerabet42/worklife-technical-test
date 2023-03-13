from .common import (
  client,
  reset_databases,
  basic_employee,
  basic_vacation_type,
  basic_vacation,
  check_and_json
)

def test_vacation_balance():
  reset_databases()
  
  _, employee_json = check_and_json(basic_employee("A", "B"))
  _, vac_type_json = check_and_json(basic_vacation_type("paid_leave"))
  
  _, balance_json = check_and_json(client.post("/balance", json={
    "employee_id": employee_json["id"],
    "vacation_type_id": vac_type_json["id"],
    "amount": 20
  }))
  
  check_and_json(basic_vacation(employee_json["id"], vac_type_json["id"], "2023-03-10", "2023-03-20"))
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 10
  
  check_and_json(basic_vacation(employee_json["id"], vac_type_json["id"], "2023-04-10", "2023-04-21"), 400)
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 10

  
def test_vacation_balance_when_updating():
  reset_databases()
  
  _, employee_json = check_and_json(basic_employee("A", "B"))
  _, vac_type_json = check_and_json(basic_vacation_type("paid_leave"))
  
  _, balance_json = check_and_json(client.post("/balance", json={
    "employee_id": employee_json["id"],
    "vacation_type_id": vac_type_json["id"],
    "amount": 20
  }))
  
  _, vac_json = check_and_json(basic_vacation(employee_json["id"], vac_type_json["id"], "2023-03-10", "2023-03-20"))
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 10
  
  check_and_json(client.post(f"/vacation/{vac_json['id']}?end_date=2023-03-22"))
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 8
  
  
  _, vac_type_json = check_and_json(basic_vacation_type("other_leave"))
  
  _, balance_json = check_and_json(client.post("/balance", json={
    "employee_id": employee_json["id"],
    "vacation_type_id": vac_type_json["id"],
    "amount": 20
  }))
  
  _, vac_json = check_and_json(basic_vacation(employee_json["id"], vac_type_json["id"], "2023-04-10", "2023-04-20"))
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 10
  
  check_and_json(client.post(f"/vacation/{vac_json['id']}?end_date=2023-04-18"))
  
  _, balance_json = check_and_json(client.get(f"/balance/{balance_json['id']}"))
  assert balance_json["amount"] == 12
  
  