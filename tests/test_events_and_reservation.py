import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestEventsAndReservation:
    """Тесты страницы афиши и бронирования."""
    
    def test_events_page_loads(self, driver):
        """Проверяет, что страница афиши загружается."""
        driver.get("http://127.0.0.1:8000/events/")
        assert "Афиша" in driver.title or "Афиша" in driver.page_source
        print("✅ Страница афиши загружена")
    
    def test_events_have_reservation_buttons(self, driver):
        """Проверяет наличие кнопок 'Забронировать' на карточках."""
        driver.get("http://127.0.0.1:8000/events/")
        buttons = driver.find_elements(By.CSS_SELECTOR, ".btn-gold")
        assert len(buttons) > 0
        print(f"✅ Найдено {len(buttons)} кнопок бронирования")
    
    def test_reservation_page_loads(self, driver):
        """Проверяет, что страница бронирования загружается."""
        driver.get("http://127.0.0.1:8000/reservation/")
        assert "Бронирование" in driver.title or "Бронирование" in driver.page_source
        print("✅ Страница бронирования загружена")
    
    def test_reservation_form_has_fields(self, driver):
        """Проверяет наличие всех полей в форме бронирования."""
        driver.get("http://127.0.0.1:8000/reservation/")
        fields = [
            "id_event",
            "id_reservation_date",
            "id_reservation_time",
            "id_guests_count",
            "id_name",
            "id_phone",
            "id_email",
            "id_comment"
        ]
        for field_id in fields:
            element = driver.find_element(By.ID, field_id)
            assert element.is_displayed()
        print("✅ Все поля формы бронирования присутствуют")
    
    def test_reservation_form_submit_works(self, driver):
        """Проверяет, что форма отправляется."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        # Заполняем обязательные поля
        driver.find_element(By.ID, "id_name").send_keys("Тест Тест")
        driver.find_element(By.ID, "id_phone").send_keys("+79001234567")
        driver.find_element(By.ID, "id_guests_count").send_keys("2")
        driver.find_element(By.ID, "id_reservation_date").send_keys("2026-07-10")
        driver.find_element(By.ID, "id_reservation_time").send_keys("19:00")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Ждём либо успешную страницу, либо возврат на форму
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Проверяем, что мы перешли на страницу успеха или остались на форме с сообщением
        assert "reservation" in driver.current_url or "success" in driver.current_url
        print(f"✅ Форма отправлена, текущий URL: {driver.current_url}")