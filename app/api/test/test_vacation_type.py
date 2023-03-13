from uuid import UUID

from .common import (
  client,
  TestClient,
  reset_databases,
  basic_vacation_type
)

def test_add_vacation_type_and_delete():
  reset_databases()
  
  vac_type1_res = basic_vacation_type("paid_leave")
  vac_type2_res = basic_vacation_type("unpaid_leave")
  
  assert vac_type1_res.status_code == 200
  assert vac_type2_res.status_code == 200
  
  vac_types_res = client.get("/vacation_type")
  assert vac_types_res.status_code == 200
  vac_types_json = vac_types_res.json()
  
  assert len(vac_types_json) == 2
  assert vac_types_json[0]["name"] == "paid_leave"
  assert vac_types_json[1]["name"] == "unpaid_leave"
  
  vac_type1_res = client.delete(f"/vacation_type/{vac_types_json[0]['id']}")
  
  vac_types_res = client.get("/vacation_type")
  assert vac_types_res.status_code == 200
  vac_types_json = vac_types_res.json()
  
  assert len(vac_types_json) == 1