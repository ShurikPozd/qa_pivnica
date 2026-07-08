import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import sqlite3
import os
from datetime import datetime
import logging

# ============================================================
# 1. НАСТРОЙКА ЛОГИРОВАНИЯ
# ============================================================

def setup_logging():
    """Настраивает логирование для тестов."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Инициализируем логгер при загрузке модуля
logger = setup_logging()
logger.info("=" * 60)
logger.info("🚀 ЗАПУСК ТЕСТОВ")
logger.info("=" * 60)


# ============================================================
# 2. ФИКСТУРЫ
# ============================================================

@pytest.fixture(scope="function")
def driver(request):
    """
    Создаёт и закрывает браузер для каждого теста.
    При падении теста делает скриншот.
    """
    logger.info(f"🔧 Запуск теста: {request.node.name}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(5)
        driver.maximize_window()
        
        logger.info(f"✅ Браузер запущен для теста: {request.node.name}")
        
        yield driver
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске браузера: {e}")
        raise
    
    finally:
        # Если тест упал — делаем скриншот
        if hasattr(request, 'node') and hasattr(request.node, 'rep_call'):
            if request.node.rep_call.failed:
                screenshot_dir = "screenshots_fail"
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(screenshot_dir, f"fail_{timestamp}_{request.node.name}.png")
                try:
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"📸 Скриншот сохранён: {screenshot_path}")
                except Exception as e:
                    logger.error(f"❌ Не удалось сохранить скриншот: {e}")
        
        driver.quit()
        logger.info(f"🔚 Браузер закрыт для теста: {request.node.name}")


@pytest.fixture(scope="function")
def mobile_driver(request):
    """
    Создаёт браузер в режиме эмуляции мобильного устройства (iPhone 12).
    При падении теста делает скриншот.
    """
    logger.info(f"📱 Запуск мобильного теста: {request.node.name}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Эмуляция iPhone 12
    mobile_emulation = {
        "deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(5)
        
        logger.info(f"✅ Мобильный браузер запущен для теста: {request.node.name}")
        
        yield driver
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске мобильного браузера: {e}")
        raise
    
    finally:
        # Если тест упал — делаем скриншот
        if hasattr(request, 'node') and hasattr(request.node, 'rep_call'):
            if request.node.rep_call.failed:
                screenshot_dir = "screenshots_fail"
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(screenshot_dir, f"mobile_fail_{timestamp}_{request.node.name}.png")
                try:
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"📸 Мобильный скриншот сохранён: {screenshot_path}")
                except Exception as e:
                    logger.error(f"❌ Не удалось сохранить мобильный скриншот: {e}")
        
        driver.quit()
        logger.info(f"🔚 Мобильный браузер закрыт для теста: {request.node.name}")


@pytest.fixture(scope="session")
def api_base_url():
    """Базовый URL для API-тестов."""
    url = "http://127.0.0.1:8000"
    logger.info(f"🌐 Базовый URL API: {url}")
    return url


@pytest.fixture(scope="function")
def db_connection():
    """Создаёт подключение к БД."""
    logger.info("🗄️ Подключение к базе данных")
    
    # Путь к БД сайта
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "pivnica_portal", "db.sqlite3")
    
    # Если не найдена — пробуем другие варианты
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), "..", "db.sqlite3")
        logger.debug(f"🔍 Пробуем путь: {db_path}")
    
    if not os.path.exists(db_path):
        logger.warning("⚠️ База данных не найдена. Пропускаем БД-тесты.")
        pytest.skip("База данных не найдена. Выполните миграции в pivnica_portal.")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        logger.info(f"✅ Подключение к БД успешно: {db_path}")
        yield conn
        conn.close()
        logger.info("🔚 Подключение к БД закрыто")
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к БД: {e}")
        raise


# ============================================================
# 3. ХУК ДЛЯ PYTEST (сохранение результата теста)
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат выполнения теста в item для использования в фикстурах."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    
    # Логируем результат теста
    if rep.when == "call":
        if rep.failed:
            logger.error(f"❌ Тест УПАЛ: {item.name}")
            logger.error(f"   Ошибка: {rep.longrepr}")
        elif rep.passed:
            logger.info(f"✅ Тест ПРОЙДЕН: {item.name}")
        else:
            logger.warning(f"⚠️ Тест ПРОПУЩЕН: {item.name}")