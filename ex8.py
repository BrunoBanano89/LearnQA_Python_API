import requests
import time

URL = "https://playground.learnqa.ru/ajax/api/longtime_job"

print("1. Создание задачи")
response_create = requests.get(URL)
data = response_create.json()

token = data.get("token")
seconds = data.get("seconds")

print(f"Токен задачи: {token}")
print(f"Время выполнения: {seconds} секунд")


print("2. Проверка готовности задачи")
response_before = requests.get(URL, params={"token": token})
status_before = response_before.json()

print(f"Статус: {status_before.get('status')}")
print(f"Есть поле 'result': {'result' in status_before}")

assert status_before.get("status") == "Job is NOT ready", "Задача уже готова"
print("Ждём")


print(f"3. Осталось {seconds} секунд")
time.sleep(seconds)
print("Ожидание завершено")


print("4. Повторная проверка")
response_after = requests.get(URL, params={"token": token})
status_after = response_after.json()

print(f"Статус: {status_after.get('status')}")
print(f"Результат: {status_after.get('result')}")

assert status_after.get("status") == "Job is ready", "Задача не готова после ожидания!"
assert "result" in status_after, "Нет поля result в ответе!"

print("Задача готова")