import pytest
import requests
from url import URL
from generator import generate_random_string
from api_methods.create_courier import CourierReg
from api_methods.login_courier import CourierLogin 
from api_methods.order import OrderMethods

# Регистрация курьера с удалением данных после теста
@pytest.fixture
def create_courier_payload():
    # Подготовка данных
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    
    # Создание курьера
    CourierReg.register_new_courier(payload)
    
    yield payload 

    courier_id = CourierLogin.get_courier_id(payload)
    
    # Удаление курьера
    if courier_id:
        requests.delete(f"{URL.CR_COURIER_ENDPOINT}/{courier_id}")

# Генерация данных курьера с удалением данных после теста
@pytest.fixture
def random_courier_data():   
    # Подготовка данных
    payload = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }
    yield payload
    # Удаление курьера
    try:
        courier_id = CourierLogin.get_courier_id(payload)
        if courier_id:
            requests.delete(f"{URL.CR_COURIER_ENDPOINT}/{courier_id}")
    except:        
        pass

# Предварительное создание заказа с последующей отменой после теста
@pytest.fixture
def create_and_cancel_order(request):    
    selected_colors = getattr(request, "param", ["BLACK"])
    
    payload = OrderMethods.get_order_payload(colors=selected_colors)
    response = OrderMethods.create_order(payload)
    track_id = response.json().get("track")
    
    yield response
    
    # Удаление заказа после теста
    if track_id:
        OrderMethods.cancel_order(track_id)

