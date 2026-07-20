import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

@allure.epic("Адаптивность")
@allure.feature("Разные разрешения экрана")
class TestResponsive:
    """Тесты адаптивности на разных разрешениях."""
    
    @allure.story("Главная страница")
    def test_homepage_on_devices(self, driver_with_resolution):
        """Проверяет главную страницу на разных устройствах."""
        driver, device = driver_with_resolution
        driver.get("http://127.0.0.1:8000")
        
        with allure.step(f"Проверяем заголовок на {device}"):
            assert "Пивница" in driver.title
        
        with allure.step(f"Проверяем кнопку 'Смотреть меню' на {device}"):
            menu_button = driver.find_element(By.CSS_SELECTOR, ".btn-gold")
            assert menu_button.is_displayed()
        
        with allure.step(f"Проверяем отображение мероприятий на {device}"):
            events = driver.find_elements(By.CSS_SELECTOR, ".card")
            print(f"✅ На {device} найдено {len(events)} мероприятий")
    
    @allure.story("Страница меню")
    def test_menu_on_devices(self, driver_with_resolution):
        """Проверяет страницу меню на разных устройствах."""
        driver, device = driver_with_resolution
        driver.get("http://127.0.0.1:8000/menu/")
        
        with allure.step(f"Проверяем категории на {device}"):
            categories = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs .nav-link")
            assert len(categories) > 0
        
        with allure.step(f"Проверяем блюда на {device}"):
            dishes = driver.find_elements(By.CSS_SELECTOR, ".card")
            assert len(dishes) > 0
    
    @allure.story("Страница бронирования")
    def test_reservation_on_devices(self, driver_with_resolution):
        """Проверяет страницу бронирования на разных устройствах."""
        driver, device = driver_with_resolution
        driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step(f"Проверяем поля формы на {device}"):
            fields = ["id_name", "id_phone", "id_guests_count"]
            for field in fields:
                assert driver.find_element(By.ID, field).is_displayed()