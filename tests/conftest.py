import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
import sqlite3
import os
from datetime import datetime
import logging
import allure
from faker import Faker

# ============================================================
# 1. НАСТРОЙКА ЛОГИРОВАНИЯ
# ============================================================

def setup_logging():
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

logger = setup_logging()
logger.info("=" * 60)
logger.info("🚀 ЗАПУСК ТЕСТОВ")
logger.info("=" * 60)

# ============================================================
# 2. FAKER
# ============================================================

@pytest.fixture(scope="session")
def fake():
    """Фикстура для генерации тестовых данных."""
    return Faker('ru_RU')

# ============================================================
# 3. ФИКСТУРА ДЛЯ БРАУЗЕРА
# ============================================================

@pytest.fixture(scope="function")
def driver(request):
    """Создаёт и закрывает браузер для каждого теста."""
    logger.info(f"🔧 Запуск теста: {request.node.name}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    chrome_driver_path = os.path.join(os.path.dirname(__file__), "..", "drivers", "chromedriver.exe")
    
    if not os.path.exists(chrome_driver_path):
        logger.warning(f"⚠️ ChromeDriver не найден по пути: {chrome_driver_path}")
        logger.info("🔄 Пробуем использовать webdriver-manager...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except Exception as e:
            logger.error(f"❌ Не удалось установить ChromeDriver: {e}")
            pytest.skip("ChromeDriver не установлен")
    else:
        logger.info(f"✅ Используем ChromeDriver: {chrome_driver_path}")
        service = Service(chrome_driver_path)
    
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(5)
        driver.maximize_window()
        
        logger.info(f"✅ Браузер запущен для теста: {request.node.name}")
        yield driver
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске браузера: {e}")
        if driver:
            screenshot_dir = "screenshots_fail"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"fail_setup_{timestamp}_{request.node.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                logger.info(f"📸 Скриншот сохранён: {screenshot_path}")
            except:
                pass
        raise
    
    finally:
        if driver:
            if hasattr(request, 'node') and hasattr(request.node, 'rep_call'):
                if request.node.rep_call.failed:
                    screenshot_dir = "screenshots_fail"
                    os.makedirs(screenshot_dir, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = os.path.join(screenshot_dir, f"fail_{timestamp}_{request.node.name}.png")
                    try:
                        driver.save_screenshot(screenshot_path)
                        logger.info(f"📸 Скриншот сохранён: {screenshot_path}")
                        allure.attach.file(
                            screenshot_path,
                            name=f"Скриншот при падении: {request.node.name}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception as e:
                        logger.error(f"❌ Не удалось сохранить скриншот: {e}")
            
            driver.quit()
            logger.info(f"🔚 Браузер закрыт для теста: {request.node.name}")

# ============================================================
# 4. ПАРАМЕТРИЗАЦИЯ РАЗРЕШЕНИЙ ЭКРАНА
# ============================================================

@pytest.fixture(params=[
    (1920, 1080, "desktop"),
    (1366, 768, "laptop"),
    (375, 812, "iphone_x"),
    (768, 1024, "tablet"),
])
def driver_with_resolution(request):
    """Фикстура с разными разрешениями экрана."""
    width, height, device = request.param
    logger.info(f"📱 Тест на устройстве: {device} ({width}x{height})")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    chrome_driver_path = os.path.join(os.path.dirname(__file__), "..", "drivers", "chromedriver.exe")
    
    if not os.path.exists(chrome_driver_path):
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
    else:
        service = Service(chrome_driver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_window_size(width, height)
        driver.implicitly_wait(5)
        
        yield driver, device
        
    finally:
        driver.quit()
        logger.info(f"🔚 Браузер закрыт для устройства: {device}")

# ============================================================
# 5. ОСТАЛЬНЫЕ ФИКСТУРЫ
# ============================================================

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
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "pivnica_portal", "db.sqlite3")
    
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), "..", "db.sqlite3")
        logger.debug(f"🔍 Пробуем путь: {db_path}")
    
    if not os.path.exists(db_path):
        logger.warning("⚠️ База данных не найдена. Пропускаем БД-тесты.")
        pytest.skip("База данных не найдена")
    
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
# 6. ХУК ДЛЯ PYTEST
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат выполнения теста."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    
    if rep.when == "call":
        if rep.failed:
            logger.error(f"❌ Тест УПАЛ: {item.name}")
            logger.error(f"   Ошибка: {rep.longrepr}")
        elif rep.passed:
            logger.info(f"✅ Тест ПРОЙДЕН: {item.name}")
        else:
            logger.warning(f"⚠️ Тест ПРОПУЩЕН: {item.name}")