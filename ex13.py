import pytest
import requests

test_data = [
    (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        {"platform": "Mobile", "browser": "No", "device": "Android"}
    ),
    (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1",
        {"platform": "Mobile", "browser": "Chrome", "device": "iOS"}
    ),
    (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        {"platform": "Unknown", "browser": "Unknown", "device": "Unknown"}
    ),
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        {"platform": "Web", "browser": "Chrome", "device": "No"}
    ),
    (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        {"platform": "Mobile", "browser": "No", "device": "iOS"}
    )
]

URL = "https://playground.learnqa.ru/ajax/api/user_agent_check"


class TestUserAgent:
    @pytest.mark.parametrize("user_agent, expected", test_data)
    def test_user_agent_check(self, user_agent, expected):
        response = requests.get(URL, headers={"User-Agent": user_agent})
        actual = response.json()

        error_messages = []
        if actual.get("platform") != expected["platform"]:
            error_messages.append(f"platform: ожидалось '{expected['platform']}', получено '{actual.get('platform')}'")
        if actual.get("browser") != expected["browser"]:
            error_messages.append(f"browser: ожидалось '{expected['browser']}', получено '{actual.get('browser')}'")
        if actual.get("device") != expected["device"]:
            error_messages.append(f"device: ожидалось '{expected['device']}', получено '{actual.get('device')}'")

        if error_messages:
            pytest.fail(f"Для User Agent: {user_agent}\n" + "\n".join(error_messages))