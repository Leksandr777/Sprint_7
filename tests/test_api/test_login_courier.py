import pytest
import requests
import allure

class TestLoginCourier:

    @allure.title("Тестирование api логина курьера")
    @allure.feature("Логин курьера")
    @allure.story("Успешный логин")
    def test_login_courier_success(self, base_url,new_courier):


        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }

        with allure.step("Отправка POST‑запроса для логина курьера"):
           response = requests.post(f"{base_url}/courier/login", data=payload)

        with allure.step("Проверка статус кода"):        
            assert response.status_code == 200, (f"Неверный статус код, получен {response.status_code}")
        with allure.step("Проверка что id есть в ответе"):
          assert  "id" in  response.text, (f"Неверное тело ответа, получено: {response.json()}")

    @allure.feature("Логин курьера")
    @allure.story("ЛОгин курьера с пропущенными обязательными полями")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_required_fields(self, base_url,new_courier, missing_field):
        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }
        del payload[missing_field]
        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(f"{base_url}/courier", data=payload)
        response_data = response.json()
        with allure.step("Проверка статус кода"): 
            assert response.status_code == 400, (f"Неверный статус для отсутствующего поля {missing_field}")
        with allure.step("Проверка сообщения об ошибке"):
            assert response_data["message"]== "Недостаточно данных для создания учетной записи",(f"В ответе нет сообщения о незаполненных полях")

    @allure.feature("Логин курьера")
    @allure.story("ЛОгин курьера с пустыми обязательными полями")
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_login_with_empty_required_fields(self, base_url,new_courier, empty_field):
        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }
        payload[empty_field]=""

        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(f"{base_url}/courier", data=payload)
        response_data = response.json()

        with allure.step("Проверка статус кода"): 
            assert response.status_code == 400, (f"Неверный статус для отсутствующего поля {empty_field}")
        with allure.step("Проверка сообщения об ошибке"):        
            assert response_data["message"]== "Недостаточно данных для создания учетной записи",(f"В ответе нет сообщения о незаполненных полях")

    @allure.feature("Логин курьера")
    @allure.story("Попытка логина несуществующего курьера")
    def test_login_unspecified_user(self, base_url):

        payload = {
            "login": "Unspecified_test_user123",
            "password": "Unspecified_password_user123",
        }
        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(f"{base_url}/courier/login", data=payload)
        response_data = response.json() 
        with allure.step("Проверка статус кода"):               
            assert response.status_code == 404, (f"Неверный статус код, получен {response.status_code}")
        with allure.step("Проверка сообщения об ошибке"):                  
            assert response_data["message"]== "Учетная запись не найдена",(f"В ответе нет сообщения о незаполненных полях")

