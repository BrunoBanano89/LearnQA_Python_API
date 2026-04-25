import time
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):

    @allure.title("Attempt to delete user with ID 2 (protected user)")
    @allure.description("Try to delete user ID 2 using auth from vinkotov - should be forbidden")
    def test_delete_user_id_2_forbidden(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        user_id_to_delete = 2
        response_delete = MyRequests.delete(
            f"/user/{user_id_to_delete}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_delete, 400)
        error_message = response_delete.json().get("error", "")
        assert error_message == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Unexpected error message: {error_message}"

    @allure.title("Positive delete user scenario")
    @allure.description("Create user, auth as this user, delete, then verify user is deleted")
    def test_positive_delete_created_user(self):
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response_register, 200)
        Assertions.assert_json_has_key(response_register, "id")

        user_id = self.get_json_value(response_register, "id")
        email = register_data["email"]
        password = register_data["password"]

        login_data = {
            "email": email,
            "password": password
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_delete, 200)

        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response_get, 404)
        assert response_get.content.decode("utf-8") == "User not found", \
            f"User with ID {user_id} still exists after deletion!"

    @allure.title("Attempt to delete user by another user")
    @allure.description("Create user A, create user B, auth as B, try to delete user A - should be forbidden")
    def test_delete_user_by_another_user_forbidden(self):
        register_data1 = self.prepare_registration_data()
        response_register1 = MyRequests.post("/user/", data=register_data1)
        Assertions.assert_code_status(response_register1, 200)
        user_id1 = self.get_json_value(response_register1, "id")
        email1 = register_data1["email"]
        password1 = register_data1["password"]

        time.sleep(1)

        register_data2 = self.prepare_registration_data()
        response_register2 = MyRequests.post("/user/", data=register_data2)
        Assertions.assert_code_status(response_register2, 200)
        email2 = register_data2["email"]
        password2 = register_data2["password"]

        login_data = {
            "email": email2,
            "password": password2
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        response_delete = MyRequests.delete(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response_delete, 200)

        login_data1 = {
            "email": email1,
            "password": password1
        }
        response_login1 = MyRequests.post("/user/login", data=login_data1)
        Assertions.assert_code_status(response_login1, 200)