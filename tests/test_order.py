import pytest
#import allure

from api_methods.order import OrderMethods

class TestOrder:

    #@allure.title("Код ответа 201 при успешном создании заказа")    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors_success_201(self, color):       
        payload = OrderMethods.get_order_payload(colors=color)
        response = OrderMethods.create_order(payload)       
        
        track_id = response.json().get("track")

        try:            
            assert response.status_code == 201            
        
        finally:           
            if track_id:
                OrderMethods.cancel_order(track_id)

    #@allure.title("Тело ответа содержит слово 'track' при успешном создании заказа")    
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors_success_track(self, color):       
        payload = OrderMethods.get_order_payload(colors=color)
        response = OrderMethods.create_order(payload)       
        
        track_id = response.json().get("track")

        try:            
            assert "track" in response.json()
        
        finally:           
            if track_id:
                OrderMethods.cancel_order(track_id)

    #@allure.title("Код ответа 200 при успешном получении списка заказов")      
    def test_get_orders_list_returns_orders_in_body_200(self, create_and_cancel_order):        
        response = OrderMethods.get_orders_list()        
        
        assert response.status_code == 200        

    #@allure.title("Вывод массива при успешном получении списка заказов")    
    def test_get_orders_list_returns_orders_in_body_array(self, create_and_cancel_order):        
        response = OrderMethods.get_orders_list()      
                
        assert isinstance(response.json()["orders"], list)
        # Теперь мы на 100% уверены, что список не пустой
        assert len(response.json()["orders"]) > 0

    #@allure.title("В полученном списке есть заказы")      
    def test_get_orders_list_returns_orders_in_body_list(self, create_and_cancel_order):        
        response = OrderMethods.get_orders_list()     
              
        assert len(response.json()["orders"]) > 0