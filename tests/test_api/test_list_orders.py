import pytest
import requests
import allure

class TestGetListOrders:

    @allure.title("Тестирование api списка заказов")
    @allure.feature("Получение списка заказов")
    @allure.story("Успешное получение списка заказов")
    def test_get_list_orders_success(self, base_url):

        payload = {

                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
            }
        orders_track = []
        with allure.step("Создание 5 тестовых заказов для гарантированного непустого списка"):
            for i in range(5):
                payload["firstName"] = f"Naturo{i}"
                response = requests.post(f"{base_url}/orders", data=payload)
                assert response.status_code == 201, "Не удалось создать тестовый заказ"

            order_data = response.json()
            orders_track.append(order_data["track"]) 

        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(f"{base_url}/orders")

        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, (f"Неверный статус код ответа")
        response_data = response.json()
        with allure.step("Проверка, что ответ является списком"):
            assert isinstance(response_data["orders"], list), "Поле 'orders' должно быть списком"

        orders_ids=[]
        orders_list = response_data["orders"]
        if orders_list:
            for order in orders_list:
                orders_ids.append(order["id"])
        with allure.step("Проверка, что список непустой"):
            assert len(orders_ids)>0, "Список пуст"
