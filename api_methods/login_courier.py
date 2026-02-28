import requests
import allure

from url import URL

class CourierLogin:

    @staticmethod
    @allure.step("Авторизация курьера")
    def login_courier(payload):        
        return requests.post(URL.LOG_COURIER_ENDPOINT, json=payload)
    
    @classmethod
    @allure.step("Получение id курьера")
    def get_courier_id(cls, payload):        
        response = cls.login_courier(payload)
        if response.status_code == 200:
            return response.json().get("id")
        return None
