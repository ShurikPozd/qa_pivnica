import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

@allure.epic("Негативные тесты")
@allure.feature("Валидация формы бронирования")
class TestNegative:
    """Негативные тесты."""
    
    def test_empty_form_submission(self, driver):
        """Проверяет отправку пустой формы."""
        with allure.step("Открываем страницу бронирования"):
            driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step("Отправляем пустую форму"):
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Проверяем, что остались на странице"):
            assert "/reservation/success/" not in driver.current_url
            assert "/reservation/" in driver.current_url
    
    def test_invalid_phone(self, driver, fake):
        """Проверяет валидацию телефона (слишком короткий)."""
        with allure.step("Открываем страницу бронирования"):
            driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step("Заполняем форму с невалидным телефоном"):
            driver.find_element(By.ID, "id_name").send_keys(fake.name())
            driver.find_element(By.ID, "id_phone").send_keys("123")
            driver.find_element(By.ID, "id_guests_count").send_keys("1")
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Проверяем, что форма не отправилась"):
            assert "/reservation/success/" not in driver.current_url
    
    def test_invalid_email(self, driver, fake):
        """Проверяет валидацию email."""
        with allure.step("Открываем страницу бронирования"):
            driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step("Заполняем форму с невалидным email"):
            driver.find_element(By.ID, "id_name").send_keys(fake.name())
            driver.find_element(By.ID, "id_phone").send_keys(fake.phone_number())
            driver.find_element(By.ID, "id_email").send_keys("not-an-email")
            driver.find_element(By.ID, "id_guests_count").send_keys("1")
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Проверяем, что форма не отправилась"):
            assert "/reservation/success/" not in driver.current_url
    
    def test_missing_name(self, driver, fake):
        """Проверяет валидацию обязательного поля 'Имя'."""
        with allure.step("Открываем страницу бронирования"):
            driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step("Заполняем форму без имени"):
            driver.find_element(By.ID, "id_phone").send_keys(fake.phone_number())
            driver.find_element(By.ID, "id_guests_count").send_keys("2")
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Проверяем, что форма не отправилась"):
            assert "/reservation/success/" not in driver.current_url
    
    def test_missing_phone(self, driver, fake):
        """Проверяет валидацию обязательного поля 'Телефон'."""
        with allure.step("Открываем страницу бронирования"):
            driver.get("http://127.0.0.1:8000/reservation/")
        
        with allure.step("Заполняем форму без телефона"):
            driver.find_element(By.ID, "id_name").send_keys(fake.name())
            driver.find_element(By.ID, "id_guests_count").send_keys("2")
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", submit_button)
        
        with allure.step("Проверяем, что форма не отправилась"):
            assert "/reservation/success/" not in driver.current_url