import pytest
import requests
from selenium.webdriver.common.by import By

# ============================================================
# ДЫМОВЫЕ ТЕСТЫ (SMOKE) — быстрая проверка
# ============================================================

@pytest.mark.smoke
class TestSmoke:
    """Дымовые тесты для быстрой проверки."""

    def test_homepage_opens(self, driver):
        driver.get("http://127.0.0.1:8000")
        assert "Пивница" in driver.title
        print("✅ Главная открыта")

    def test_menu_opens(self, driver):
        driver.get("http://127.0.0.1:8000/menu/")
        assert "Меню" in driver.title or "Меню" in driver.page_source
        print("✅ Меню открыто")

    def test_events_opens(self, driver):
        driver.get("http://127.0.0.1:8000/events/")
        assert "Афиша" in driver.title or "Афиша" in driver.page_source
        print("✅ Афиша открыта")

    def test_reservation_opens(self, driver):
        driver.get("http://127.0.0.1:8000/reservation/")
        assert "Бронирование" in driver.title or "Бронирование" in driver.page_source
        print("✅ Бронирование открыто")

    def test_api_works(self, api_base_url):
        response = requests.get(f"{api_base_url}/api/event-date/1/")
        assert response.status_code == 200
        print("✅ API работает")


# ============================================================
# РЕГРЕССИОННЫЕ ТЕСТЫ (REGRESSION) — полная проверка
# ============================================================

@pytest.mark.regression
class TestRegression:
    """Регрессионные тесты для полной проверки."""

    def test_homepage_has_button(self, driver):
        driver.get("http://127.0.0.1:8000")
        menu_button = driver.find_element(By.CSS_SELECTOR, ".btn-gold")
        assert menu_button.is_displayed()
        print("✅ Кнопка 'Смотреть меню' найдена")

    def test_menu_has_categories(self, driver):
        driver.get("http://127.0.0.1:8000/menu/")
        categories = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs .nav-link")
        assert len(categories) > 0
        print(f"✅ Найдено {len(categories)} категорий")

    def test_menu_has_dishes(self, driver):
        driver.get("http://127.0.0.1:8000/menu/")
        dishes = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(dishes) > 0
        print(f"✅ Найдено {len(dishes)} блюд")

    def test_reservation_form_has_fields(self, driver):
        driver.get("http://127.0.0.1:8000/reservation/")
        fields = ["id_name", "id_phone", "id_guests_count", "id_reservation_date", "id_reservation_time"]
        for field in fields:
            assert driver.find_element(By.ID, field).is_displayed()
        print("✅ Все поля формы присутствуют")

    def test_api_event_detail(self, api_base_url):
        response = requests.get(f"{api_base_url}/api/event-detail/1/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "event_date" in data
        print("✅ API мероприятия работает")


# ============================================================
# МЕДЛЕННЫЕ ТЕСТЫ (SLOW) — больше 10 секунд
# ============================================================

@pytest.mark.slow
class TestSlow:
    """Медленные тесты (> 10 секунд)."""

    def test_homepage_load_time(self, driver):
        import time
        start = time.time()
        driver.get("http://127.0.0.1:8000")
        load_time = time.time() - start
        assert load_time < 5.0, f"Главная загружается {load_time:.2f} сек"
        print(f"✅ Главная загружена за {load_time:.2f} сек")

    def test_menu_load_time(self, driver):
        import time
        start = time.time()
        driver.get("http://127.0.0.1:8000/menu/")
        load_time = time.time() - start
        assert load_time < 5.0, f"Меню загружается {load_time:.2f} сек"
        print(f"✅ Меню загружено за {load_time:.2f} сек")