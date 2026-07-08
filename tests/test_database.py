import pytest

class TestDatabase:
    """Тесты базы данных."""
    
    def test_categories_table_exists(self, db_connection):
        """Проверяет существование таблицы категорий."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portal_category'")
        result = cursor.fetchone()
        assert result is not None
        print("✅ Таблица категорий существует")
    
    def test_dishes_table_exists(self, db_connection):
        """Проверяет существование таблицы блюд."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portal_dish'")
        result = cursor.fetchone()
        assert result is not None
        print("✅ Таблица блюд существует")
    
    def test_events_table_exists(self, db_connection):
        """Проверяет существование таблицы мероприятий."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portal_event'")
        result = cursor.fetchone()
        assert result is not None
        print("✅ Таблица мероприятий существует")
    
    def test_customers_table_exists(self, db_connection):
        """Проверяет существование таблицы клиентов."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portal_customer'")
        result = cursor.fetchone()
        assert result is not None
        print("✅ Таблица клиентов существует")
    
    def test_reservations_table_exists(self, db_connection):
        """Проверяет существование таблицы бронирований."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portal_reservation'")
        result = cursor.fetchone()
        assert result is not None
        print("✅ Таблица бронирований существует")
    
    def test_has_data_in_categories(self, db_connection):
        """Проверяет, что в категориях есть данные."""
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM portal_category")
        count = cursor.fetchone()[0]
        assert count > 0
        print(f"✅ В категориях {count} записей")