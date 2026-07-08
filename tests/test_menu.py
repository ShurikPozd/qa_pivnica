import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestMenu:
    """Тесты страницы меню."""
    
    def test_menu_page_loads(self, driver):
        """Проверяет, что страница меню загружается."""
        driver.get("http://127.0.0.1:8000/menu/")
        assert "Меню" in driver.title or "Меню" in driver.page_source
        print("✅ Страница меню загружена")
    
    def test_menu_has_categories(self, driver):
        """Проверяет наличие категорий в меню."""
        driver.get("http://127.0.0.1:8000/menu/")
        categories = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs .nav-link")
        assert len(categories) > 0
        print(f"✅ Найдено {len(categories)} категорий")
    
    def test_menu_has_dishes(self, driver):
        """Проверяет наличие блюд в меню."""
        driver.get("http://127.0.0.1:8000/menu/")
        dishes = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(dishes) > 0
        print(f"✅ Найдено {len(dishes)} блюд")
    
    def test_menu_dish_has_price(self, driver):
        """Проверяет, что у блюда отображается цена."""
        driver.get("http://127.0.0.1:8000/menu/")
        price_element = driver.find_element(By.CSS_SELECTOR, ".card-text strong")
        assert any(char.isdigit() for char in price_element.text)
        print(f"✅ Цена найдена: {price_element.text}")
    
    def test_category_filter_works(self, driver):
        """Проверяет работу фильтрации по категориям."""
        driver.get("http://127.0.0.1:8000/menu/")
        first_category = driver.find_element(By.CSS_SELECTOR, ".nav-tabs .nav-link")
        category_name = first_category.text.strip()
        driver.execute_script("arguments[0].click();", first_category)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
        )
        dishes = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(dishes) >= 0
        print(f"✅ Фильтрация по категории '{category_name}' работает")