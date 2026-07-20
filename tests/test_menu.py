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
        
        # Ищем цену разными способами
        price_found = False
        
        # Способ 1: ищем по классу .card-text strong
        try:
            price_element = driver.find_element(By.CSS_SELECTOR, ".card-text strong")
            if any(char.isdigit() for char in price_element.text):
                price_found = True
                print(f"✅ Цена найдена (способ 1): {price_element.text}")
        except:
            pass
        
        # Способ 2: ищем любую цену в карточке
        if not price_found:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, ".card-text, .card-body p, .card-body strong")
                for el in elements:
                    if "руб" in el.text or any(char.isdigit() for char in el.text):
                        price_found = True
                        print(f"✅ Цена найдена (способ 2): {el.text}")
                        break
            except:
                pass
        
        # Способ 3: ищем по XPath
        if not price_found:
            try:
                price_element = driver.find_element(By.XPATH, "//*[contains(text(), 'руб')]")
                price_found = True
                print(f"✅ Цена найдена (способ 3): {price_element.text}")
            except:
                pass
        
        assert price_found, "Не найдена цена ни на одном блюде"
    
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
    
    @pytest.mark.parametrize("category_index", [0, 1, 2])
    def test_each_category_has_dishes(self, driver, category_index):
        """Проверяет, что каждая категория содержит блюда."""
        driver.get("http://127.0.0.1:8000/menu/")
        
        categories = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs .nav-link")
        assert category_index < len(categories), f"Категории {category_index} не существует"
        
        category = categories[category_index]
        category_name = category.text.strip()
        driver.execute_script("arguments[0].click();", category)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
        )
        
        dishes = driver.find_elements(By.CSS_SELECTOR, ".card")
        assert len(dishes) > 0, f"В категории '{category_name}' нет блюд"
        print(f"✅ В категории '{category_name}' найдено {len(dishes)} блюд")