import pytest
import requests
import allure
import helpers

class TestLoginCourier:
    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1//courier/login"
    @allure.title("Тестирование api логина курьера")
    @allure.feature("Логин курьера")
    @allure.story("Успешный логин")
    def test_login_courier_success(self):
        new_courier = helpers.create_new_courier()

        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }

        with allure.step("Отправка POST‑запроса для логина курьера"):
           response = requests.post(self.BASE_URL, data=payload)

        with allure.step("Проверка статус кода"):        
            assert response.status_code == 200, (f"Неверный статус код, получен {response.status_code}")
        with allure.step("Проверка что id есть в ответе"):
          assert  "id" in  response.text, (f"Неверное тело ответа, получено: {response.json()}")

    @allure.feature("Логин курьера")
    @allure.story("ЛОгин курьера с пропущенными обязательными полями")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_required_fields(self, missing_field):
        new_courier = helpers.create_new_courier()
        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }
        del payload[missing_field]
        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json()
        with allure.step("Проверка статус кода"): 
            assert response.status_code == 400, (f"Неверный статус для отсутствующего поля {missing_field}")
        with allure.step("Проверка сообщения об ошибке"):
            assert response_data["message"]== "Недостаточно данных для входа",(f"В ответе нет сообщения о незаполненных полях")

    @allure.feature("Логин курьера")
    @allure.story("ЛОгин курьера с пустыми обязательными полями")
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_login_with_empty_required_fields(self, empty_field):
        new_courier = helpers.create_new_courier()
        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
        }
        payload[empty_field]=""

        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json()

        with allure.step("Проверка статус кода"): 
            assert response.status_code == 400, (f"Неверный статус для отсутствующего поля {empty_field}")
        with allure.step("Проверка сообщения об ошибке"):        
            assert response_data["message"]== "Недостаточно данных для входа",(f"В ответе нет сообщения о незаполненных полях")

    @allure.feature("Логин курьера")
    @allure.story("Попытка логина несуществующего курьера")
    def test_login_unspecified_user(self):

        payload = {
            "login": "Unspecified_test_user123",
            "password": "Unspecified_password_user123",
        }
        with allure.step("Отправка POST‑запроса для логина курьера"):
            response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json() 
        with allure.step("Проверка статус кода"):               
            assert response.status_code == 404, (f"Неверный статус код, получен {response.status_code}")
        with allure.step("Проверка сообщения об ошибке"):                  
            assert response_data["message"]== "Учетная запись не найдена",(f"В ответе нет сообщения о незаполненных полях")

