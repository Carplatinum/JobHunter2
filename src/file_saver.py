from abc import ABC, abstractmethod
from typing import List
from src.vacancy import Vacancy
from src.config import VACANCY_FILE
import json
import os

# Сначала объявляем абстрактный класс
class VacancyFileSaver(ABC):
    """
    Абстрактный класс для работы с файлами вакансий.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass


    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        pass


    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


# Затем класс-наследник
class JSONSaver(VacancyFileSaver):
    """
    Класс для работы с JSON-файлом вакансий.
    """


    def __init__(self, filename: str = VACANCY_FILE) -> None:  # Используем значение из .env
        self.__filename = filename


    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save_to_file(vacancies)


    def get_vacancies(self) -> List[Vacancy]:
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Vacancy(**item) for item in data]


    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self._save_to_file(vacancies)


    def _save_to_file(self, vacancies: List[Vacancy]) -> None:
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump([v.as_dict() for v in vacancies], f, ensure_ascii=False, indent=2)
