import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def create_new_courier():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    courier_data = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{BASE_URL}/courier", data=payload)

    if response.status_code == 201:
        courier_data.append(login)
        courier_data.append(password)
        courier_data.append(first_name)

    return courier_data

def delete_courier(login, password):
    login_payload = {"login": login, "password": password}
    login_response = requests.post(f"{BASE_URL}/courier/login", data=login_payload)
    
    courier_id = login_response.json().get("id")
    if not courier_id:
        return

    requests.delete(f"{BASE_URL}/courier/{courier_id}")