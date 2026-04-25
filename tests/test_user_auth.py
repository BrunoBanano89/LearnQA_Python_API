import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("User Management")
@allure.feature("User Registration")
class TestUserRegister(BaseCase):

    @allure.story("Positive registration")
    @allure.title("Create new user successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.story("Negative registration - duplicate email")
    @allure.title("Create user with existing email - should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists"

    @allure.story("Negative registration - invalid email")
    @allure.title("Create user with email without @ symbol - should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_invalid_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email=email)
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format"

    @allure.story("Negative registration - missing fields")
    @allure.title("Create user without required field - should fail")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('missing_field', ['password', 'username', 'firstName', 'lastName', 'email'])
    def test_create_user_without_required_field(self, missing_field):
        data = self.prepare_registration_data()
        del data[missing_field]
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.story("Negative registration - short username")
    @allure.title("Create user with 1-character username - should fail")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_very_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)

    @allure.story("Negative registration - long username")
    @allure.title("Create user with 251-character username - should fail")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_user_with_very_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a' * 251
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)