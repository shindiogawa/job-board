import json


def test_create_job(client,normal_user_token_headers):
  data = {
    "title": "Test Create Job",
    "company": "Test company",
    "company_url": "https://testcreatejob.com",
    "location":"Test location",
    "description":"Test description",
    "date_posted":"2022-07-20"
  }

  response = client.post("/job/create-job",json.dumps(data), headers=normal_user_token_headers)
  assert response.status_code == 200
  assert response.json()["company"] == "Test company"
  assert response.json()["description"] == "Test description"


def test_retrieve_job_by_id(client):
  data = {
    "title": "Test Create Job",
    "company": "Test company",
    "company_url": "https://testcreatejob.com",
    "location":"Test location",
    "description":"Test description",
    "date_posted":"2022-07-20"
  }
  client.post("job/create-job",json.dumps(data))
  response = client.get("/job/get/1")
  assert response.status_code == 200
  assert response.json()["title"] == "Test Create Job"