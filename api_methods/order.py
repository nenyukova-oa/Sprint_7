import requests
import allure

from url import URL
from data import TestData

class OrderMethods:

    @staticmethod
    @allure.step("Формирования тела запроса для создания заказа")
    def get_order_payload(colors=None):
        payload = TestData.ORDER_PAYLOAD.copy()
        if colors is not None:
            payload["color"] = colors
        return payload
    
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(payload):
        return requests.post(URL.ORDER_ENDPOINT, json=payload)
    
    @staticmethod
    @allure.step("Отмена заказа")  
    def cancel_order(track_id):     
        return requests.put(URL.CANCEL_ORDER_ENDPOINT, json={"track": track_id})

    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders_list():
        return requests.get(URL.ORDER_ENDPOINT)