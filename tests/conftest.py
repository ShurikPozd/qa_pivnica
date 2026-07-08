import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import sqlite3
import os

# --- Фикстуры для Selenium ---

@pytest.fixture(scope="function")
def driver():
    """Создаёт и закрывает браузер для каждого теста."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Убери эту строку, если хочешь видеть браузер
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

# --- Фикстура для API ---

@pytest.fixture(scope="session")
def api_base_url():
    """Базовый URL для API-тестов."""
    return "http://127.0.0.1:8000"

# --- Фикстура для БД ---

@pytest.fixture(scope="function")
def db_connection():
    """Создаёт подключение к БД."""
    import os
    # Путь к БД сайта
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "pivnica_portal", "db.sqlite3")
    
    # Если не найдена — пробуем другие варианты
    if not os.path.exists(db_path):
        # Может быть в корне проекта
        db_path = os.path.join(os.path.dirname(__file__), "..", "db.sqlite3")
    
    if not os.path.exists(db_path):
        # Если БД нет — пропускаем тесты БД
        pytest.skip("База данных не найдена. Выполните миграции в pivnica_portal.")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()