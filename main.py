import logging
import os

from dotenv import load_dotenv

from src.api import HeadHunterAPI
from src.config import LOG_LEVEL
from src.file_saver import JSONSaver
from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.vacancy import Vacancy

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)
load_dotenv()


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    Позволяет искать, фильтровать, сохранять и удалять вакансии.
    """
    vacancy_file = os.getenv("VACANCY_FILE", "data/vacancies.json")
    default_per_page = int(os.getenv("DEFAULT_PER_PAGE", 20))

    hh_api = HeadHunterAPI()
    json_saver = JSONSaver(filename=vacancy_file)
    vacancies_list = []

    while True:
        print("\nМеню:")
        print("1. Найти вакансии и сохранить в файл")
        print("2. Показать все сохранённые вакансии")
        print("3. Показать топ N вакансий по зарплате")
        print("4. Фильтровать вакансии по ключевому слову в описании")
        print("5. Фильтровать вакансии по диапазону зарплат")
        print("6. Удалить вакансию по названию")
        print("0. Выйти")
        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            try:
                per_page = int(input(f"Сколько вакансий загрузить "
                                     f"(по умолчанию {default_per_page}): ") or default_per_page)
            except ValueError:
                per_page = default_per_page
            try:
                vacancies_json = hh_api.get_vacancies(query, per_page=per_page)
                vacancies_list = Vacancy.cast_to_object_list(vacancies_json)
                for v in vacancies_list:
                    json_saver.add_vacancy(v)
                print(f"Загружено и сохранено {len(vacancies_list)} вакансий.")
            except Exception as e:
                print(f"Ошибка при получении вакансий: {e}")

        elif choice == "2":
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
            else:
                print_vacancies(vacancies)

        elif choice == "3":
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            except ValueError:
                print("Некорректное число.")
                continue
            sorted_vacancies = sort_vacancies(vacancies)
            top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
            print_vacancies(top_vacancies)

        elif choice == "4":
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").split()
            filtered = filter_vacancies(vacancies, filter_words)
            print_vacancies(filtered)

        elif choice == "5":
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            salary_range = input("Введите диапазон зарплат (например, 100000-150000): ")
            ranged = get_vacancies_by_salary(vacancies, salary_range)
            print_vacancies(ranged)

        elif choice == "6":
            vacancies = json_saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            title = input("Введите точное название вакансии для удаления: ")
            found = [v for v in vacancies if v.title == title]
            if not found:
                print("Вакансия не найдена.")
            else:
                for v in found:
                    json_saver.delete_vacancy(v)
                print("Вакансия удалена.")

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Некорректный выбор. Повторите попытку.")


if __name__ == "__main__":
    user_interaction()
