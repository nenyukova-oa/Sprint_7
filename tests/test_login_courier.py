import pytest
import allure

from api_methods.login_courier import CourierLogin
from generator import generate_random_string
from data import TestData

class TestCourierLogin:

    @allure.title("Код 200 при авторизации курьера с валидными данными")    
    def test_courier_login_success_200(self, create_courier_payload):
        response = CourierLogin.login_courier(create_courier_payload)
        
        assert response.status_code == 200
        
    @allure.title("Возвращение id при авторизации курьера с валидными данными")     
    def test_courier_login_success_id(self, create_courier_payload):        
        response = CourierLogin.login_courier(create_courier_payload)        
        
        assert response.json().get("id") is not None

    @allure.title("Код ошибки 404 при указании неправильного логина или пароля")    
    @pytest.mark.parametrize("field_to_change", ["login", "password"])
    def test_login_with_wrong_credentials_fail_404(self, create_courier_payload, field_to_change):        
        wrong_payload = create_courier_payload.copy()
        wrong_payload[field_to_change] = generate_random_string(10)
        
        response = CourierLogin.login_courier(wrong_payload)
        
        assert response.status_code == 404        

    
    @pytest.mark.parametrize("field_to_change", ["login", "password"])
    def test_login_with_wrong_credentials_fail_little_data(self, create_courier_payload, field_to_change): 
        allure.dynamic.title(f"Сообщение '{TestData.text_log_not_found}' при указании неправильного логина или пароля")       
        wrong_payload = create_courier_payload.copy()
        wrong_payload[field_to_change] = generate_random_string(10)
        
        response = CourierLogin.login_courier(wrong_payload)        
        
        assert response.json()["message"] == TestData.text_log_not_found     

    @allure.title("Код ошибки 400 при незаполненном обязательном поле")    
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_fail_400(self, create_courier_payload, missing_field):
        
        incomplete_payload = create_courier_payload.copy()
        incomplete_payload.pop(missing_field)
        
        response = CourierLogin.login_courier(incomplete_payload)
        
        assert response.status_code == 400      

    
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_required_field_fail_little_data(self, create_courier_payload, missing_field):
        allure.dynamic.title(f"Сообщение '{TestData.text_log_little_data}' при незаполненном обязательном поле")
        incomplete_payload = create_courier_payload.copy()
        incomplete_payload.pop(missing_field)
        
        response = CourierLogin.login_courier(incomplete_payload)        
        
        assert response.json()["message"] == TestData.text_log_little_data 

    @allure.title("Ошибка 404 при авторизации под несуществующим пользователем")    
    def test_login_non_existent_courier_fail_404(self):        
        random_payload = {
            "login": generate_random_string(15),
            "password": generate_random_string(15)
        }
        
        response = CourierLogin.login_courier(random_payload)
        
        assert response.status_code == 404

    
    def test_login_non_existent_courier_fail_(self):
        allure.dynamic.title(f"Сообщение '{TestData.text_log_not_found}' при авторизации под несуществующим пользователем")        
        random_payload = {
            "login": generate_random_string(15),
            "password": generate_random_string(15)
        }
        
        response = CourierLogin.login_courier(random_payload)        
        
        assert response.json()["message"] == TestData.text_log_not_found
