import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Changed Name"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_not_auth(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register, 200)
        user_id = self.get_json_value(response_register, "id")

        new_name = "Hacked Name"
        response_edit = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_edit, 400)

    def test_edit_user_by_another_user(self):
        # Регистрируем пользователя №1
        register_data1 = self.prepare_registration_data()
        response_register1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response_register1, 200)
        user_id1 = self.get_json_value(response_register1, "id")

        # Регистрируем пользователя №2
        register_data2 = self.prepare_registration_data()
        response_register2 = MyRequests.post("/user/", data=register_data2)
        Assertions.assert_code_status(response_register2, 200)
        email2 = register_data2["email"]
        password2 = register_data2["password"]

        # Логинимся под пользователем №2
        login_data = {
            "email": email2,
            "password": password2
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # Пытаемся редактировать пользователя №1
        new_name = "Malicious Name"
        response_edit = MyRequests.put(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response_edit, 200)

        # Проверяем данные пользователя №1 (должны быть только публичные поля)
        response_get = MyRequests.get(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response_get, "username")
        Assertions.assert_json_has_not_key(response_get, "email")
        Assertions.assert_json_has_not_key(response_get, "firstName")
        Assertions.assert_json_has_not_key(response_get, "lastName")

    def test_edit_email_without_at_sign(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register, 200)
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response_register, "id")

        login_data = {
            "email": email,
            "password": password
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        invalid_email = "invalid_email_example.com"
        response_edit = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": invalid_email}
        )

        Assertions.assert_code_status(response_edit, 400)
        error_message = response_edit.json().get("error", "")
        assert error_message == "Invalid email format", \
            f"Unexpected error message: {error_message}"

    def test_edit_firstname_too_short(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register, 200)
        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response_register, "id")

        login_data = {
            "email": email,
            "password": password
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        short_name = "A"
        response_edit = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": short_name}
        )

        Assertions.assert_code_status(response_edit, 400)
        error_message = response_edit.json().get("error", "")
        assert error_message == "The value for field `firstName` is too short", \
            f"Unexpected error message: {error_message}"