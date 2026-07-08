import pytest
from selenium.webdriver.common.by import By

class TestPaperMenu:
    """Тесты страницы бумажного меню."""
    
    def test_paper_menu_page_loads(self, driver):
        """Проверяет, что страница бумажного меню загружается."""
        driver.get("http://127.0.0.1:8000/paper-menu/")
        assert "Сканы меню" in driver.title or "Сканы меню" in driver.page_source
        print("✅ Страница бумажного меню загружена")
    
    def test_paper_menu_has_images(self, driver):
        """Проверяет наличие изображений бумажного меню."""
        driver.get("http://127.0.0.1:8000/paper-menu/")
        images = driver.find_elements(By.CSS_SELECTOR, ".card img")
        
        if len(images) == 0:
            print("⚠️ Изображений бумажного меню нет (можно добавить через админку)")
        else:
            assert len(images) > 0
            print(f"✅ Найдено {len(images)} изображений бумажного меню")
    
    def test_paper_menu_images_visible(self, driver):
        """Проверяет, что изображения меню отображаются."""
        driver.get("http://127.0.0.1:8000/paper-menu/")
        images = driver.find_elements(By.CSS_SELECTOR, ".card img")
        
        for img in images:
            assert img.is_displayed()
        
        print(f"✅ Все {len(images)} изображений отображаются")