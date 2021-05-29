import json


def test_create_job(client):
  data = {
    "title": "Test Create Job",
    "company": "Test company",
    "company_url": "https://testcreatejob.com",
    "location":"Test location",
    "description":"Test description",
    "date_posted":"2022-07-20"
  }

  response = client.post("/job/create-job",json.dumps(data))
  assert response.status_code == 200
