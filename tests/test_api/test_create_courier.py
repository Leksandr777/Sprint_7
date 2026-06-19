import pytest
import requests
import random
import allure
import helpers

class TestCreateCourier:

    BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1/courier"

    @allure.title("Тестирование api создания курьера")
    @allure.feature("Создание курьера")
    @allure.story("Успешное создание курьера")
    def test_create_courier_success(self):
        login = f"test_login_{random.randint(1, 9999)}"
        password = f"test_pass_{random.randint(1, 9999)}"
        first_name = f"TestName_{random.randint(1, 9999)}"

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        with allure.step("Отправка POST‑запроса для создания курьера"):
            response = requests.post(self.BASE_URL, data=payload)

        with allure.step("Проверка статус кода"):
            assert response.status_code == 201, (f"Неверный статус код, получен {response.status_code}")
        with allure.step("Проверка тела ответа"):            
            assert response.json() == {"ok": True}, (f"Неверное тело ответа, получено: {response.json()}")

    @allure.feature("Создание курьера")
    @allure.story("Попытка создания дубликата курьера")
    def test_create_duplicate_courier(self):
        new_courier = helpers.create_new_courier()

        payload = {
            "login": new_courier[0],
            "password": new_courier[1],
            "firstName": new_courier[2]
        }
        response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 409, (f"Не получен статус конфликта, статус {response.status_code}")
        with allure.step("Проверка сообщения об ошибке"):                 
            assert response_data["message"] == "Этот логин уже используется. Попробуйте другой.", (f"Нет сообщения о конфликте, получено: {response.json()}")

    @allure.feature("Создание курьера")
    @allure.story("Проверка создания с пропущенными полями") 
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_without_required_fields(self, missing_field):
        payload = {
            "login": f"test_login_{random.randint(1, 9999)}",
            "password": f"test_pass_{random.randint(1, 9999)}",
            "firstName": f"TestName_{random.randint(1, 9999)}"
        }
        del payload[missing_field]
        with allure.step(f"Отправка запроса без поля {missing_field}"):
            response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 400, (f"Неверный статус для отсутствующего поля {missing_field}")
        with allure.step("Проверка сообщения об ошибке"):      
            assert response_data["message"]== "Недостаточно данных для создания учетной записи",(f"В ответе нет сообщения о незаполненных полях")

    @allure.feature("Создание курьера")
    @allure.story("Проверка создания с пустыми полями") 
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_empty_fields(self,  empty_field):

        payload = {
            "login": f"test_login_{random.randint(1, 9999)}",
            "password": f"test_pass_{random.randint(1, 9999)}",
            "firstName": f"TestName_{random.randint(1, 9999)}"
        }
        payload[empty_field]=''
        with allure.step(f"Отправка запроса с пустым полем {empty_field}"):
           response = requests.post(self.BASE_URL, data=payload)
        response_data = response.json()
        with allure.step("Проверка статус кода"):
            assert response.status_code == 400, (f"Неверный статус для пустых полей")
        with allure.step("Проверка сообщения об ошибке"):      
            assert response_data["message"]== "Недостаточно данных для создания учетной записи",(f"В ответе нет сообщения о незаполненных полях")
