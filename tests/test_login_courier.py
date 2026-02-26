import pytest
import allure

from api_methods.login_courier import CourierLogin
from generator import generate_random_string
from data import TestData

class TestCourierLogin:

    @allure.title("Код ответа 200 и возвращение id курьера в теле ответа при авторизации курьера с валидными данными")    
    def test_courier_login_success_200(self, create_courier_payload):
        response = CourierLogin.login_courier(create_courier_payload)
        
        assert response.status_code == 200
        assert response.json().get("id") is not None      


    @pytest.mark.parametrize("field_to_change", ["login", "password"])
    def test_login_with_wrong_credentials_fail_little_data(self, create_courier_payload, field_to_change): 
        allure.dynamic.title(f"Код ответа 404 и сообщение '{TestData.text_log_not_found}' в теле ответа при указании неправильного логина или пароля при авторизации")       
        wrong_payload = create_courier_payload.copy()
        wrong_payload[field_to_change] = generate_random_string(10)
        
        response = CourierLogin.login_courier(wrong_payload)        
        
        assert response.status_code == 404
        assert response.json()["message"] == TestData.text_log_not_found    
   
    
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field_fail_little_data(self, create_courier_payload, missing_field):
        allure.dynamic.title(f"Код ответа 400, сообщение '{TestData.text_log_little_data}' в теле ответа при незаполненном обязательном поле")
        incomplete_payload = create_courier_payload.copy()
        incomplete_payload.pop(missing_field)
        
        response = CourierLogin.login_courier(incomplete_payload)        
        
        assert response.status_code == 400 
        assert response.json()["message"] == TestData.text_log_little_data 

    
    def test_login_non_existent_courier_fail_(self):
        allure.dynamic.title(f"Код ответа 404, сообщение '{TestData.text_log_not_found}' в теле ответа при авторизации под несуществующим пользователем")        
        random_payload = {
            "login": generate_random_string(15),
            "password": generate_random_string(15)
        }
        
        response = CourierLogin.login_courier(random_payload)        
        
        assert response.status_code == 404
        assert response.json()["message"] == TestData.text_log_not_found
