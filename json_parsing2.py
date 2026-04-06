import json

string_s_json_format = '{"answer": "Hello, User"}'
obj = json.loads(string_s_json_format)

key= "answer"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} в JSON нет")