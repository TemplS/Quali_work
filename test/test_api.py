import requests
from data_base import base_url
from data_base import heads
import allure


@allure.title("Поиск по ID")
@allure.description("Проверяем работоспособность сайта искать фильмы по ID")
@allure.story("Поиск")
def test_find_by_id(film_id: int = 196707):
    req = requests.get(base_url + f'{film_id}', headers=heads)
    assert req.status_code == 200


@allure.title("Поиск без токена")
@allure.description(
    "Проверяем работоспособность сайта, если не подставить токен авторизации")
@allure.story("Поиск")
def test_find_without_token(name: str = "Spider-man"):
    req = requests.get(base_url + "search/" + f'{name}')
    assert req.status_code == 401


@allure.title("Поиск на английском языке")
@allure.description("Проверяем поиск фильмов и сериалов на английском языке")
@allure.story("Поиск")
def test_find_in_english(name: str = "Pirates of the Caribbean"):
    req = requests.get(base_url + "search/" + f'{name}', headers=heads)
    assert req.status_code == 200


@allure.title("Поиск с несуществующим/вымышленным ID")
@allure.description("Проверяем поиск с вымышленным ID фильма")
@allure.story("Поиск")
def test_find_with_unreal_id(film_id: int = 000000):
    req = requests.get(base_url + f'{film_id}', headers=heads)
    assert req.status_code == 200


@allure.title("Поиск по неправильному методу")
@allure.description(
    "Проверяем поиск с использованием неверно выбранного метода")
@allure.story("Поиск")
def test_find_other_method(name: str = "Spider-man"):
    req = requests.post(base_url + "search/" + f'{name}')
    assert req.status_code == 401
