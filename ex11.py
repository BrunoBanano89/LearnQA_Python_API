import requests
def test_cookie():
    url = "https://playground.learnqa.ru/api/homework_cookie"
    response = requests.get(url)
    cookies = response.cookies

    for cookie_name, cookie_value in cookies.items():
        print(f"cookie: name = '{cookie_name}', value = '{cookie_value}'")
        assert response.cookies.get('HomeWork') == 'hw_value'