import requests

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1
print("1. Запрос без параметра method:")
response_no_method = requests.get(URL)
print(f"Ответ: {response_no_method.text}\n")

# 2
print("2. Запрос не из списка:")
response_head = requests.head(URL)
print(f"Ответ: {response_head.text if response_head.text else '(пустой ответ)'}\n")

# 3
print("3. Запрос с правильным method (GET с method=GET):")
response_correct = requests.get(URL, params={"method": "GET"})
print(f"Ответ: {response_correct.text}\n")

# 4
print("4. Поиск несоответствий:")

http_methods = ["GET", "POST", "PUT", "DELETE"]
method_values = ["GET", "POST", "PUT", "DELETE"]

for http_method in http_methods:
    for param_value in method_values:
        if http_method == "GET":
            response = requests.get(URL, params={"method": param_value})
        else:
            response = requests.request(http_method, URL, data={"method": param_value})

        is_success = (response.text == '{"success":"!"}')
        is_match = (http_method == param_value)

        if is_success and not is_match:
            print(f"Несоответствие: {http_method}-запрос с method={param_value} -> {response.text}")
        elif not is_success and is_match:
            print(f"Несоответствие: {http_method}-запрос с method={param_value} -> {response.text}")