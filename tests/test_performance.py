import pytest
import time

class TestPerformance:
    """Тесты производительности."""
    
    def test_homepage_load_time(self, driver):
        """Проверяет время загрузки главной страницы (< 3 сек)."""
        start = time.time()
        driver.get("http://127.0.0.1:8000")
        load_time = time.time() - start
        
        assert load_time < 3.0, f"Главная загружается слишком долго: {load_time:.2f} сек"
        print(f"✅ Главная загружена за {load_time:.2f} сек")
    
    def test_menu_load_time(self, driver):
        """Проверяет время загрузки страницы меню (< 3 сек)."""
        start = time.time()
        driver.get("http://127.0.0.1:8000/menu/")
        load_time = time.time() - start
        
        assert load_time < 3.0, f"Меню загружается слишком долго: {load_time:.2f} сек"
        print(f"✅ Меню загружено за {load_time:.2f} сек")
    
    def test_events_load_time(self, driver):
        """Проверяет время загрузки страницы афиши (< 3 сек)."""
        start = time.time()
        driver.get("http://127.0.0.1:8000/events/")
        load_time = time.time() - start
        
        assert load_time < 3.0, f"Афиша загружается слишком долго: {load_time:.2f} сек"
        print(f"✅ Афиша загружена за {load_time:.2f} сек")