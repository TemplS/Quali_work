from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from data_base import kino_url
import allure


driver = webdriver.Chrome()
driver.implicitly_wait(120)
driver.maximize_window()


@allure.title("Поиск случайного фильма")
@allure.story("Поисковая строка")
def test_find_random_film():
    with allure.step("Переход на сайт"):
        driver.get(kino_url)
        driver.find_element(By.ID, "js-button").click()
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".styles_root__wLB_G")))
    with allure.step("Нажимаем кнопку поиска"):
        driver.find_element(By.CSS_SELECTOR,
                            ".styles_root__wLB_G").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#search")))
    with allure.step("Нажимаем кнопку Случайный фильм"):
        driver.find_element(By.CSS_SELECTOR,
                            "#search").click()
    with allure.step("Проверяем, что появилась информация о фильме"):
        fail = driver.find_element(By.CSS_SELECTOR,
                                   ".info").is_displayed()
        assert fail == True


@allure.title("Переход на вкладку авторизации")
@allure.story("Авторизация")
def test_open_auth():
    driver.switch_to.new_window()
    with allure.step("Переход на сайт"):
        driver.get(kino_url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".styles_loginButton__6_QNl")))
    with allure.step("Нажимаем кнопку Войти"):
        driver.find_element(By.CSS_SELECTOR,
                            ".styles_loginButton__6_QNl").click()
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".passp-auth-content")))
    with allure.step(
            "Проверяем, что открылось окно авторизации"):
        info = driver.find_element(By.CSS_SELECTOR,
                                   ".passp-auth-content").is_displayed()
        assert info == True


@allure.title("Переход на вкладку телеканалы -> Спортивные")
@allure.story("Телеканалы")
def test_sport_tv_channels():
    driver.switch_to.new_window()
    with allure.step("Переход на сайт"):
        driver.get(kino_url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, '[href="https://hd.kinopoisk.ru/channels"]')))
    with ((allure.step("Нажимаем кнопку Войти"))):
        driver.find_element(By.CSS_SELECTOR,
                            '[href="https://hd.kinopoisk.ru/channels"]').click()
    with allure.step("Нажимаем кнопку Спортивные"):
        driver.find_element(By.XPATH,
                            "//button[text()='Спортивные']").click()
    with allure.step("Проверяем, что находимся на правильной ссылке"):
        url = driver.current_url
        assert url == "https://hd.kinopoisk.ru/channels?channelCategoryTab=3"


@allure.title("Поиск фильмов на русском языке")
@allure.story("Поисковая строка")
def test_find_films_in_russian(film_name: str = "Ёлки"):
    driver.switch_to.new_window()
    with allure.step("Переход на сайт"):
        driver.get(kino_url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, "[role='combobox']")))
    with (allure.step("Вводим данные в поисковую строку и нажимаем Return")):
        driver.find_element(By.CSS_SELECTOR,
                            "[role='combobox']").send_keys(
            f'{film_name}' + Keys.RETURN)
    with allure.step(
            "Сравниваем наш запрос с тем, что выдало по нашему запросу"):
        name = driver.find_element(By.CSS_SELECTOR, "b").text
        assert name == f"{film_name}"


@allure.title("Использование фильтров расширенного поиска")
@allure.story("Расширенный поиск")
def test_find_in_advanced_mode(actor_name: str = "Анджелина Джоли",
                               year: int = 2012):
    driver.switch_to.new_window()
    with allure.step("Переход на сайт"):
        driver.get(kino_url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, '[aria-label="Расширенный поиск"]')))
    with allure.step("Нажимаем кнопку Расширенного поиска"):
        driver.find_element(By.CSS_SELECTOR,
                            ".styles_advancedSearch__gn_09").click()
    with allure.step("Вводим год фильма"):
        driver.find_element(By.CSS_SELECTOR,
                            "#year").send_keys(f"{year}")
    with allure.step("Вводим имя актёра/актрисы"):
        driver.find_element(By.CSS_SELECTOR, ".el_9").send_keys(actor_name)
    with allure.step("Нажимаем кнопку Поиск"):
        driver.find_element(By.CSS_SELECTOR,
                            ".el_18").click()
    with allure.step("Сравниваем год каждого фильма с веденным"):
        films = driver.find_elements(By.CSS_SELECTOR, ".year")
        for film in films:
            assert film.text == f'{year}'

    driver.quit()
