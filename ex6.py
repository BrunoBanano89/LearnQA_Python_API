import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect')
redirect_count = len(response.history)
final_url = response.url

print(f"Количество редиректов: {redirect_count}")
print(f"Итоговый url: {final_url}")