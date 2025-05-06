import os
from typing import Generator

import pytest

from src.file_saver import JSONSaver
from src.vacancy import Vacancy

TEST_FILE = "tests/test_vacancies.json"


@pytest.fixture(autouse=True)
def cleanup() -> Generator[None, None, None]:
    """
    Удаляет тестовый файл до и после каждого теста.
    """
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_add_and_get_vacancy() -> None:
    """
    Проверяет добавление и получение вакансии через JSONSaver.
    """
    saver = JSONSaver(filename=TEST_FILE)
    vacancy = Vacancy("Test", "http://test", 100000, "desc")
    saver.add_vacancy(vacancy)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test"
    assert vacancies[0].salary == 100000


def test_no_duplicate_vacancy() -> None:
    """
    Проверяет, что дублирующая вакансия не добавляется повторно.
    """
    saver = JSONSaver(filename=TEST_FILE)
    vacancy = Vacancy("Test", "http://test", 100000, "desc")
    saver.add_vacancy(vacancy)
    saver.add_vacancy(vacancy)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1


def test_delete_vacancy() -> None:
    """
    Проверяет удаление вакансии из файла.
    """
    saver = JSONSaver(filename=TEST_FILE)
    vacancy1 = Vacancy("Test1", "http://test1", 100000, "desc1")
    vacancy2 = Vacancy("Test2", "http://test2", 200000, "desc2")
    saver.add_vacancy(vacancy1)
    saver.add_vacancy(vacancy2)
    saver.delete_vacancy(vacancy1)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test2"


def test_get_vacancies_empty_file() -> None:
    """
    Проверяет, что при отсутствии файла возвращается пустой список вакансий.
    """
    saver = JSONSaver(filename=TEST_FILE)
    vacancies = saver.get_vacancies()
    assert vacancies == []
