import requests

response = requests.get("https://playground.learnqa.ru/api/homework_header")
print(response.headers)

def test_homework_header():
    url = "https://playground.learnqa.ru/api/homework_header"
    response = requests.get(url)
    assert response.headers.get('x-secret-homework-header') == 'Some secret value'