from abc import ABC, abstractmethod
from typing import Any, Dict, List
import requests
from src.config import HH_API_URL


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий.
    """

    @abstractmethod
    def _connect(self) -> None:
        """
        Метод для подключения к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Получить вакансии по ключевому слову.
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API hh.ru.
    """

    __BASE_URL = HH_API_URL

    def __init__(self) -> None:
        self.__session = requests.Session()

    def _connect(self) -> None:
        """
        Метод подключения к API hh.ru.
        Отправляет тестовый запрос и проверяет статус ответа.
        """
        params: dict[str, str | int] = {'text': 'python', 'per_page': 1}
        response = self.__session.get(self.__BASE_URL, params=params)  # type: ignore[arg-type]
        if response.status_code != 200:
            raise ConnectionError("Не удалось подключиться к API hh.ru")

    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Получить список вакансий по ключевому слову с hh.ru.
        Вызывает метод подключения перед запросом.
        """
        self._connect()
        params: dict[str, str | int] = {
            'text': keyword,
            'per_page': per_page,
            'area': 113  # Россия
        }
        response = self.__session.get(self.__BASE_URL, params=params)  # type: ignore[arg-type]
        if response.status_code != 200:
            raise RuntimeError("Ошибка получения данных с hh.ru")
        data = response.json()
        return data.get('items', [])
