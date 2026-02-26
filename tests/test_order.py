import pytest
import allure

from api_methods.order import OrderMethods

class TestOrder:

    @allure.title("Код ответа 201 и и слово 'track' в теле ответа при успешном создании заказа")    
    @pytest.mark.parametrize("create_and_cancel_order", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ], indirect=True)

    def test_create_order_with_different_colors_success(self, create_and_cancel_order):       
        response = create_and_cancel_order

        assert response.status_code == 201
        assert "track" in response.json()
    

    @allure.title("Код ответа 200 и вывод массива с заказами в теле ответа при успешном получении списка заказов")      
    def test_get_orders_list_succes(self, create_and_cancel_order):        
        response = OrderMethods.get_orders_list()        
        
        assert response.status_code == 200 
        assert isinstance(response.json()["orders"], list)        
        assert len(response.json()["orders"]) > 0 
