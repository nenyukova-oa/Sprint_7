class URL:
    BASE_URL = "https://qa-scooter.praktikum-services.ru" # ссылка на сайт
    CR_COURIER_ENDPOINT = f"{BASE_URL}/api/v1/courier" # создание курьера
    LOG_COURIER_ENDPOINT = f"{BASE_URL}/api/v1/courier/login" # логин курьера
    ORDER_ENDPOINT = f"{BASE_URL}/api/v1/orders" # создание заказа и получение списка заказов
    CANCEL_ORDER_ENDPOINT = f"{BASE_URL}/api/v1/orders/cancel" # отмена заказа