import pytest

from django.urls import reverse


# @pytest.mark.django_db
# def test_unauthorized_request(api_client):
#     url = 'http://127.0.0.1:8000/api/token/'
#     # token = get_or_create_token()
#     token_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MjMyMzI2LCJpYXQiOjE2OTgyMTc5MjYsImp0aSI6IjM0ZjQxN2Q1Mjg5OTQzMTJiOTU0NWNjMDhmMjhlNjYzIiwidXNlcl9pZCI6NSwibmFtZSI6ImFwcGxlIn0.hm3ZRNc7cTDzyd6fbN1PRKKSFVdUgc_h4bY1bJbsJbg"
#     body = {
#         "username": "apple",
#         "password": "apple12345!"
#     }
#     headers = {'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk4MjMyMzI2LCJpYXQiOjE2OTgyMTc5MjYsImp0aSI6IjM0ZjQxN2Q1Mjg5OTQzMTJiOTU0NWNjMDhmMjhlNjYzIiwidXNlcl9pZCI6NSwibmFtZSI6ImFwcGxlIn0.hm3ZRNc7cTDzyd6fbN1PRKKSFVdUgc_h4bY1bJbsJbg'}
#     api_client.credentials(HTTP_AUTHORIZATION='Token ' + token_key)
#     response = api_client.post(url, json=body, headers=headers)
#     assert response.status_code == 400
