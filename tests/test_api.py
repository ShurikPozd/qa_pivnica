import pytest
import requests

class TestAPI:
    """Тесты API-эндпоинтов сайта 'Пивница'."""
    
    def test_event_date_api(self, api_base_url):
        """Проверяет получение даты мероприятия."""
        response = requests.get(f"{api_base_url}/api/event-date/1/")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        print(f"✅ Дата мероприятия: {data['date']}")
    
    def test_event_times_api(self, api_base_url):
        """Проверяет получение времени мероприятия."""
        response = requests.get(f"{api_base_url}/api/event-times/1/")
        assert response.status_code == 200
        data = response.json()
        assert "start_time" in data
        assert "end_time" in data
        print(f"✅ Время мероприятия: {data['start_time']} - {data['end_time']}")
    
    def test_event_detail_api(self, api_base_url):
        """Проверяет получение деталей мероприятия."""
        response = requests.get(f"{api_base_url}/api/event-detail/1/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "description" in data
        assert "event_date" in data
        print(f"✅ Детали мероприятия: {data['name']}")
    
    def test_event_date_api_404(self, api_base_url):
        """Проверяет обработку несуществующего мероприятия."""
        response = requests.get(f"{api_base_url}/api/event-date/9999/")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        print("✅ Ошибка 404 обработана корректно")