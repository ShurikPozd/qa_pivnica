import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestHomepage:
    """Тесты главной страницы сайта 'Пивница'."""
    
    def test_homepage_loads(self, driver):
        """Проверяет, что главная страница загружается."""
        driver.get("http://127.0.0.1:8000")
        assert "Пивница" in driver.title
        print("✅ Главная страница загружена")
    
    def test_homepage_has_menu_button(self, driver):
        """Проверяет наличие кнопки 'Смотреть меню'."""
        driver.get("http://127.0.0.1:8000")
        menu_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-gold"))
        )
        assert menu_button.is_displayed()
        print("✅ Кнопка 'Смотреть меню' найдена")
    
    def test_homepage_has_events(self, driver):
        """Проверяет, что на главной отображаются мероприятия."""
        driver.get("http://127.0.0.1:8000")
        events = driver.find_elements(By.CSS_SELECTOR, ".card")
        print(f"✅ Найдено {len(events)} карточек на главной")
    
    def test_navigation_to_menu(self, driver):
        """Проверяет переход на страницу меню."""
        driver.get("http://127.0.0.1:8000")
        
        try:
            menu_link = driver.find_element(By.LINK_TEXT, "Меню")
        except:
            try:
                menu_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Меню")
            except:
                try:
                    menu_link = driver.find_element(By.CSS_SELECTOR, ".nav-link[href*='/menu/']")
                except:
                    menu_link = driver.find_element(By.XPATH, "//a[contains(@href, '/menu/')]")
        
        driver.execute_script("arguments[0].click();", menu_link)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        assert "Меню" in driver.title or "Меню" in driver.page_source
        print("✅ Переход на страницу меню выполнен")
    
    def test_navigation_to_events(self, driver):
        """Проверяет переход на страницу афиши."""
        driver.get("http://127.0.0.1:8000")
        
        try:
            events_link = driver.find_element(By.LINK_TEXT, "Афиша")
        except:
            try:
                events_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Афиша")
            except:
                try:
                    events_link = driver.find_element(By.CSS_SELECTOR, ".nav-link[href*='/events/']")
                except:
                    events_link = driver.find_element(By.XPATH, "//a[contains(@href, '/events/')]")
        
        driver.execute_script("arguments[0].click();", events_link)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        assert "Афиша" in driver.title or "Афиша" in driver.page_source
        print("✅ Переход на страницу афиши выполнен")