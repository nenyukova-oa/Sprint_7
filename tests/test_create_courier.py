import pytest
import allure

from api_methods.create_courier import CourierReg
from api_methods.login_courier import CourierLogin
from generator import generate_random_string
from data import TestData


class TestCreateCourier:

    @allure.title("Успешное создание курьера при заполнении всех полей валидными данными")    
    def test_courier_created_success_all_fields(self, random_courier_data):
        response = CourierReg.register_new_courier(random_courier_data)       
        courier_id = CourierLogin.get_courier_id(random_courier_data)   
             
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        assert courier_id is not None

    @allure.title("Успешное создание курьера при пустом поле Имя и валидных данных в остальных полях")
    def test_create_courier_without_firstname_success(self, random_courier_data):
        payload = random_courier_data.copy()
        payload.pop("firstName")      
        response = CourierReg.register_new_courier(payload) 
        courier_id = CourierLogin.get_courier_id(random_courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        assert courier_id is not None

    @allure.title("Код ответа 201, сообщение 'ok: True' в теле ответа при успешной регистрации")    
    def test_create_courier_success_returns_valid_response(self, random_courier_data):
        response = CourierReg.register_new_courier(random_courier_data)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
    def test_create_duplicate_courier_fail_returns_valid_response(self, create_courier_payload):
        allure.dynamic.title(f"Код ответа 409, сообщение '{TestData.text_create_duplicate}' в теле ответа при регистрации существующего курьера")        
        response = CourierReg.register_new_courier(create_courier_payload)
        
        assert response.status_code == 409
        assert response.json()["message"] == TestData.text_create_duplicate      
        
    
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fail_little_data(self, random_courier_data, missing_field):  
        allure.dynamic.title(f"Код ответа 400, сообщение '{TestData.text_create_missing_field}' в теле ответа при отсутствии поля: {missing_field}")      
        payload = random_courier_data.copy()      
        payload.pop(missing_field)       
        response = CourierReg.register_new_courier(payload)        
        
        assert response.status_code == 400
        assert response.json()["message"] == TestData.text_create_missing_field

               
    def test_create_courier_with_existing_login_fail_wrong_login(self, create_courier_payload):  
        allure.dynamic.title(f"Код ответа 409, сообщение '{TestData.text_create_duplicate}' в теле ответа при регистрации пользователя с существующим логином")       
        existing_login = create_courier_payload["login"]
        
        
        duplicate_payload = {
            "login": existing_login,
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }        
        
        response = CourierReg.register_new_courier(duplicate_payload)
        
        assert response.status_code == 409
        assert response.json()["message"] == TestData.text_create_duplicate