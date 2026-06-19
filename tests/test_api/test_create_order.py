import pytest
import requests
import allure

class TestCreateOrder:

    @allure.title("Тестирование api создания заказа")
    @allure.feature("Создание заказа")
    @allure.story("Успешное создание заказа")
    @pytest.mark.parametrize("colour_option", [
        {"colors": ["BLACK"]},
        {"colors": ["GREY"]},  
        {"colors": ["BLACK", "GREY"]},
        {"colors": []} 
    ])
    def test_create_order_with_different_colours(self, base_url, colour_option):

        payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
            }

        if colour_option["colors"]:
            payload["colors"] = colour_option["colors"]
        with allure.step("Отправка POST‑запроса для создания заказа"):
           response = requests.post(f"{base_url}/orders", data=payload)

        with allure.step("Проверка статус кода"):
           assert response.status_code == 201, (f"Неверный код статуса создания заказа ")

        response_data = response.json()
        with allure.step("Проверка тела ответа"): 
          assert "track" in response_data, "В ответе отсутствует поле 'track'"


