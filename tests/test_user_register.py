import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

# РЕГА (новый)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

# РЕГА (существующий email)
    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content: {response.content}"

# РЕГА (без символа @)
    def test_create_user_with_invalid_email(self):
        email = 'vinkotov.example.com'  # нет символа @
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content: {response.content}"

# РЕГА (без указания одного из полей)
    @pytest.mark.parametrize('missing_field', ['password', 'username', 'firstName', 'lastName', 'email'])
    def test_create_user_without_required_field(self, missing_field):
        data = self.prepare_registration_data()
        del data[missing_field]

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
            f"Unexpected response content: {response.content}"

# РЕГА (с очень коротким именем)
    def test_create_user_with_very_short_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a'  # имя из одного символа

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", \
            f"Unexpected response content: {response.content}"

# РЕГА (с очень длинным именем)
    def test_create_user_with_very_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'a' * 251  # имя из 251 символа

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", \
            f"Unexpected response content: {response.content}"