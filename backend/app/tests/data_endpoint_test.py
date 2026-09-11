import requests

def test_endpoint():

    response = requests.get("http://localhost:8000/endpoint_test/new_data_stream/205d9ed7-76d1-45b4-8d9d-569ac4337918")
    return response.text

print(test_endpoint())