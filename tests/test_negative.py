import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestNegative:
    """Негативные тесты (проверка обработки ошибок)."""
    
    def test_empty_form_submission(self, driver):
        """Проверяет отправку пустой формы бронирования."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что мы остались на странице бронирования (не ушли на success)
        assert "/reservation/success/" not in driver.current_url
        assert "/reservation/" in driver.current_url
        print("✅ Пустая форма не отправилась (остались на странице)")
    
    def test_invalid_phone(self, driver):
        """Проверяет валидацию телефона (слишком короткий)."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        driver.find_element(By.ID, "id_name").send_keys("Тест")
        driver.find_element(By.ID, "id_phone").send_keys("123")  # Некорректный телефон
        driver.find_element(By.ID, "id_guests_count").send_keys("1")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что форма не отправилась
        assert "/reservation/success/" not in driver.current_url
        print("✅ Некорректный телефон не прошёл валидацию")
    
    def test_guests_count_zero(self, driver):
        """Проверяет валидацию количества гостей (0)."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        driver.find_element(By.ID, "id_name").send_keys("Тест")
        driver.find_element(By.ID, "id_phone").send_keys("+79001234567")
        driver.find_element(By.ID, "id_guests_count").clear()
        driver.find_element(By.ID, "id_guests_count").send_keys("0")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что не ушли на success
        assert "/reservation/success/" not in driver.current_url
        print("✅ Количество гостей 0 не прошло валидацию")
    
    def test_guests_count_too_high(self, driver):
        """Проверяет валидацию количества гостей (>20)."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        driver.find_element(By.ID, "id_name").send_keys("Тест")
        driver.find_element(By.ID, "id_phone").send_keys("+79001234567")
        driver.find_element(By.ID, "id_guests_count").clear()
        driver.find_element(By.ID, "id_guests_count").send_keys("100")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что не ушли на success
        assert "/reservation/success/" not in driver.current_url
        print("✅ Слишком много гостей не прошло валидацию")
    
    def test_invalid_email(self, driver):
        """Проверяет валидацию email."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        driver.find_element(By.ID, "id_name").send_keys("Тест")
        driver.find_element(By.ID, "id_phone").send_keys("+79001234567")
        driver.find_element(By.ID, "id_email").send_keys("not-an-email")
        driver.find_element(By.ID, "id_guests_count").send_keys("1")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что не ушли на success
        assert "/reservation/success/" not in driver.current_url
        print("✅ Некорректный email не прошёл валидацию")
    
    def test_missing_name(self, driver):
        """Проверяет валидацию обязательного поля 'Имя'."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        # Заполняем все поля, кроме имени
        driver.find_element(By.ID, "id_phone").send_keys("+79001234567")
        driver.find_element(By.ID, "id_guests_count").send_keys("2")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что не ушли на success
        assert "/reservation/success/" not in driver.current_url
        print("✅ Поле 'Имя' обязательно для заполнения")
    
    def test_missing_phone(self, driver):
        """Проверяет валидацию обязательного поля 'Телефон'."""
        driver.get("http://127.0.0.1:8000/reservation/")
        
        # Заполняем все поля, кроме телефона
        driver.find_element(By.ID, "id_name").send_keys("Тест")
        driver.find_element(By.ID, "id_guests_count").send_keys("2")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Проверяем, что не ушли на success
        assert "/reservation/success/" not in driver.current_url
        print("✅ Поле 'Телефон' обязательно для заполнения")