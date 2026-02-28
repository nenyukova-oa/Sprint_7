import requests
import allure

from url import URL

class CourierReg:

    @staticmethod
    @allure.step("Регистрация курьера")
    def register_new_courier(payload):
        return requests.post(URL.CR_COURIER_ENDPOINT, data=payload)

