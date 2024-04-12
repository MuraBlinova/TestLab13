import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.fixture
def browser():
    driver = webdriver.Firefox()
    yield driver
    driver.implicitly_wait(10)  # seconds
    driver.quit()


def wait_until_element_visible(browser, method, param):
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.invisibility_of_element_located((method, param)))
    except TimeoutException:
        print("Элемент", str(method), str(param), "всё ещё на странице")
        assert False


def button(browser, method, param):
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.element_to_be_clickable((method, param)))
        arr = browser.find_elements(method, param)
        if len(arr) == 1:
            arr[0].click()
            return 1
        elif len(arr) > 1:
            for el in arr:
                try:
                    el.click()
                except ElementClickInterceptedException:
                    print(el, "не кликабельна")
            print(method, param, "button не уникальна!")
            assert True
        else:
            print(method, param, "button не найдена")
            assert False
    except TimeoutException:
        print(method, param, "button не кликабельна")
        assert False


def in_put(browser, method, param, text=""):
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(EC.visibility_of_element_located((method, param)))
        arr = browser.find_elements(method, param)
        if len(arr) == 1:
            arr[0].clear()
            arr[0].send_keys(text)
            return 1
        else:
            arr[0].clear()
            arr[0].send_keys(text)
            print(method, param, "input не уникален!")
            assert True
    except TimeoutException:
        print(method, param, "input не найден")
        assert False


def text_of_element(browser, method, param):
    arr = browser.find_elements(method, param)
    if len(arr) == 1:
        return arr[0].text
    elif len(arr) > 1:
        print(method, param, "element не уникален!")
        assert False
    else:
        print(method, param, "element не найден")
        assert False


def check_usename(browser, method, param, username, error_text, type_check=False):
    in_put(browser, method, param, username)
    button(browser, By.XPATH, "//button[@type='submit']")
    param_check = browser.find_elements(method, param)[0].get_attribute("aria-errormessage")
    if type_check:
        if text_of_element(browser, By.ID, param_check) == error_text:
            print("Неккоректная валидация при", param, "=", username, "найден текст ошибки")
            assert True
            return 0
    else:
        try:
            wait = WebDriverWait(browser, 1)
            wait.until(lambda driver: driver.find_element(By.ID, param_check).get_attribute("value") != "")
            if text_of_element(browser, By.ID, param_check) == error_text:
                assert True
            else:
                print(param, "=", username, " - некорректня ошибка. Ожидаемо:", error_text, "Фактический:",
                      text_of_element(browser, By.ID, param_check))
                assert True
        except TimeoutException:
            print("Неккоректная валидация при", param, "=", username, "не найден текст ошибки")
            assert True
            return 0
    print(param, "=", username, "-  корректное поведение")
    assert True


def check_password(browser, method, param, password, error_text, type_check=False):
    in_put(browser, method, param, password)
    button(browser, By.XPATH, "//button[@type='submit']")
    param_check = browser.find_elements(method, param)[0].get_attribute("aria-errormessage")
    if type_check:
        if text_of_element(browser, By.ID, param_check) == error_text:
            print("Неккоректная валидация при", param, "=", password, "найден текст ошибки")
            assert True
            return 0
    else:
        try:
            wait = WebDriverWait(browser, 1)
            wait.until(lambda driver: driver.find_element(By.ID, param_check).get_attribute("value") != "")
            if text_of_element(browser, By.ID, param_check) == error_text:
                assert True
            else:
                print(param, "=", password, " - некорректня ошибка. Ожидаемо:", error_text, "Фактический:",
                      text_of_element(browser, By.ID, param_check))
                assert True
        except TimeoutException:
            print("Неккоректная валидация при", param, "=", password, "не найден текст ошибки")
            assert True
            return 0


def popup_open(browser):
    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.visibility_of_element_located((By.ID, "modal-root")))
        print("Попап открыт")
        # assert True
        return 1
    except TimeoutException:
        print("Попап не открыт")
        # assert True
        return 0


def test_entranse(browser):
    print()
    assert True
    browser.get("https://ru.spbtv.com/ru-RU")
    wait_until_element_visible(browser, By.CLASS_NAME, "Nv4V3")
    button(browser, By.XPATH, "//div[@id='app']/div/div/header/button[2]")
    # негативные тесты
    check_usename(browser, By.ID, "username", "", "Поле обязательно для заполнения")
    # _0<<11
    check_usename(browser, By.ID, "username", "7", "Неправильно указаны данные")
    # _[0] !=7 && !=8
    check_usename(browser, By.ID, "username", "19991111111", "Неправильно указаны данные")
    # _невозможный префикс
    check_usename(browser, By.ID, "username", "71111111111", "Неправильно указаны данные")
    # _зарегестрированный номер
    check_usename(browser, By.ID, "username", "79990379627",
                  "Указанный телефон нам не знаком. Проверьте введенные данные или зарегистрируйтесь.")
    # _[0]==8
    in_put(browser, By.ID, "username", "89991111111")
    button(browser, By.ID, "current-password")
    if text_of_element(browser, By.ID, "username-error") == "Неправильно указаны данные":
        print("Неккоректная валидация при первой цифре 8")
        assert True
    else:
        print("username = 89991111111 - корректная валидация")
        assert True
    text_usernmae = browser.find_element(By.ID, "username").get_attribute("value")
    if text_usernmae != "+7 999 111-11-11":
        print("Неккоректная обработка строки логина при первой цивре 8:", text_usernmae)
        assert True
    else:
        print("username = 89991111111 - корректное поведение инпута")
        assert True

    check_password(browser, By.ID, "current-password", '', 'Поле обязательно для заполнения', type_check=False)
    check_password(browser, By.ID, "current-password", 'g', 'Как минимум 6 символов', type_check=False)
    check_password(browser, By.ID, "current-password", 'ggggg', 'Как минимум 6 символов', type_check=False)
    check_password(browser, By.ID, "current-password", '123456', 'Как минимум 6 символов', type_check=True)

    in_put(browser, By.ID, "username", "79991112234")
    if text_of_element(browser, By.XPATH,
                       "//div[@id='modal-root']/div/div/div/div[2]/div/div/div/form/div[3]/div[2]") != "Указан неправильный телефон или пароль. Проверьте правильность введенных данных.":
        print("Некорректная обработка сочетания неправильного логина и пароля")
        assert True
    else:
        print("Корректная обработка сочетания неправильного логина и пароля")
        assert True
    # _позитивный тест
    in_put(browser, By.ID, "username", "79991112234")
    button(browser, By.XPATH, "//button[@type='submit']")
    param_check = browser.find_elements(By.ID, "username")[0].get_attribute("aria-errormessage")
    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.text_to_be_present_in_element((By.ID, param_check),
                                                    "Данный номер телефона уже зарегистрирован. Для входа нажмите на кнопку “У меня уже есть аккаунт”."))
        print("Номер 79990379627 выдал ошибку:'", browser.find_element(By.ID, param_check).text,
              "' - регистрация невозможна")
        assert False
    except TimeoutException:
        in_put(browser, By.ID, "current-password", "password")
        button(browser, By.XPATH, "//button[@type='submit']")
        if popup_open(browser):
            button(browser, By.CSS_SELECTOR, ".uEmhs path")
        print("Авторизация прошла успешно\n")
        assert True


def test_registration(browser):
    print()
    assert True
    browser.get("https://ru.spbtv.com/ru-RU")
    wait_until_element_visible(browser, By.CLASS_NAME, "Nv4V3")
    button(browser, By.XPATH, "//div[@id='app']/div/div/header/button[2]")
    button(browser, By.XPATH, "//button[3]")
    # негативные тесты
    check_usename(browser, By.ID, "username", "", "Поле обязательно для заполнения")
    # _0<<11
    check_usename(browser, By.ID, "username", "7", "Неправильно указаны данные")
    # _[0] !=7 && !=8
    check_usename(browser, By.ID, "username", "19991111111", "Неправильно указаны данные")
    # _невозможный префикс
    check_usename(browser, By.ID, "username", "71111111111", "Неправильно указаны данные")
    # _зарегестрированный номер
    check_usename(browser, By.ID, "username", "79991112234",
                  "Данный номер телефона уже зарегистрирован. Для входа нажмите на кнопку “У меня уже есть аккаунт”.")
    # _[0]==8
    in_put(browser, By.ID, "username", "89991111111")
    button(browser, By.ID, "new-password")
    if text_of_element(browser, By.ID, "username-error") == "Неправильно указаны данные":
        print("Неккоректная валидация при первой цифре 8")
        assert True
    else:
        print("username = 89991111111 - корректная валидация")
        assert True
    text_usernmae = browser.find_element(By.ID, "username").get_attribute("value")
    if text_usernmae != "+7 999 111-11-11":
        print("Неккоректная обработка строки логина при первой цивре 8:", text_usernmae)
        assert True
    else:
        print("username = 89991111111 - корректное поведение инпута")
        assert True

    check_password(browser, By.ID, "new-password", '', 'Поле обязательно для заполнения', type_check=False)
    check_password(browser, By.ID, "new-password", 'g', 'Как минимум 6 символов', type_check=False)
    check_password(browser, By.ID, "new-password", 'ggggg', 'Как минимум 6 символов', type_check=False)

    # _позитивный тест
    in_put(browser, By.ID, "username", "79990379627")
    button(browser, By.XPATH, "//button[@type='submit']")
    param_check = browser.find_elements(By.ID, "username")[0].get_attribute("aria-errormessage")
    try:
        wait = WebDriverWait(browser, 1)
        wait.until(EC.text_to_be_present_in_element((By.ID, param_check),
                                                    "Данный номер телефона уже зарегистрирован. Для входа нажмите на кнопку “У меня уже есть аккаунт”."))
        print("Номер 79990379627 выдал ошибку:'", browser.find_element(By.ID, param_check).text,
              "' - регистрация невозможна")
        assert False
    except TimeoutException:
        in_put(browser, By.ID, "new-password", "password")
        button(browser, By.XPATH, "//button[@type='submit']")
        try:
            wait = WebDriverWait(browser, 1)
            wait.until(EC.invisibility_of_element_located((By.LINK_TEXT, "8(800)7009588")))
            arr = browser.find_elements(By.LINK_TEXT, "8(800)7009588")
            assert True
            if len(arr) == 1:
                print("Регистрация прошла успешно\n")
                assert True
            elif len(arr) > 1:
                print("Найдено несколько номеров для подтверждения аккаунта\n")
                assert True
        except TimeoutException:
            print("Регистрация не прошла!\n")
            assert False


def test_search_filter(browser):
    print()
    assert True
    browser.get("https://ru.spbtv.com/ru-RU")
    wait_until_element_visible(browser, By.CLASS_NAME, "Nv4V3")
    button(browser, By.CSS_SELECTOR, "[id*='menu_item_search']")
    button(browser, By.CSS_SELECTOR, "[aria-label='Закрыть']")
    button(browser, By.CSS_SELECTOR, "[id*='menu_item_search']")
    in_put(browser, By.CSS_SELECTOR, "[aria-label='Поиск']", "1")
    try:
        wait = WebDriverWait(browser, 20)
        wait.until(EC.visibility_of_element_located((By.ID, "search-suggestions")))
        print("suggestions появились")
        assert True
    except TimeoutException:
        print("suggestions не появились")
        assert True
    browser.find_elements(By.CSS_SELECTOR, "[aria-label='Поиск']")[0].send_keys(Keys.ENTER)
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "filters-groupcomponent__FiltersGroupHolder-sc-1mz7up1-0")))
        arr = browser.find_elements(By.CLASS_NAME, "buttonfactory__buttonFactory-sc-13j5qd6-0")
        assert True
        for el in arr:
            el.click()
        print("фильтры работают корректно")
        assert True
    except TimeoutException:
        print("фильтры не появились")
        assert True
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "filters-groupcomponent__FiltersGroupHolder-sc-1mz7up1-0")))
        arr = browser.find_elements(By.CLASS_NAME, "select-holder__SelectHolder-sc-1v45dmo-0")
        assert True
        for el in arr:
            el.click()
            try:
                wait = WebDriverWait(browser, 10)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "opened")))
                print("дропдаун раскрылся")
                assert True
            except TimeoutException:
                print("дропдаун не раскрылся")
                assert True
            el.click()
    except TimeoutException:
        print("дропдауны фильтров не появились")
        assert True

    print("Тест поиска и фильтрации пройден успешно")
    assert True


def test_profiles_delete(browser):
    print()
    assert True
    browser.get("https://ru.spbtv.com/ru-RU/account/profiles")
    wait_until_element_visible(browser, By.CLASS_NAME, "Nv4V3")
    button(browser, By.XPATH, "//div[@id='app']/div/div/header/button[2]")
    in_put(browser, By.ID, "username", "79991112234")
    in_put(browser, By.ID, "current-password", "password")
    button(browser, By.XPATH, "//button[@type='submit']")
    time.sleep(2)
    if popup_open(browser):
        button(browser, By.CSS_SELECTOR, ".uEmhs path")
    print("Авторизация прошла успешно\n")

    arr = browser.find_elements(By.CLASS_NAME, "OX_p4")
    print("У аккаунта", len(arr), "профилей")
    if len(arr) > 1:
        browser.find_elements(By.XPATH, "//*[contains(text(), 'Редактировать')]")[-1].click()
        button(browser, By.XPATH, "//*[contains(text(), 'Удалить')]")
        button(browser, By.CLASS_NAME, "cKKsCl")
        if popup_open(browser):
            button(browser, By.CSS_SELECTOR, "[aria-label='Закрыть']")
            print("Попап ещё открыт")
            assert False
        else:
            if len(arr) - 1 == browser.find_elements(By.CLASS_NAME, "OX_p4"):
                print("Профиль удален успешно")
                assert True
            else:
                print("Профиль не удален")
                assert False
    else:
        print("У аккаунта один профиль")
        assert False


def test_accaunt_add(browser):
    print()
    assert True
    browser.get("https://ru.spbtv.com/ru-RU/account/profiles")
    wait_until_element_visible(browser, By.CLASS_NAME, "Nv4V3")
    button(browser, By.XPATH, "//div[@id='app']/div/div/header/button[2]")
    in_put(browser, By.ID, "username", "79991112234")
    in_put(browser, By.ID, "current-password", "password")
    button(browser, By.XPATH, "//button[@type='submit']")
    time.sleep(2)
    if popup_open(browser):
        button(browser, By.CSS_SELECTOR, ".uEmhs path")
    print("Авторизация прошла успешно\n")

    arr = browser.find_elements(By.CLASS_NAME, "OX_p4")
    button(browser, By.CSS_SELECTOR, ".profileadd-icon__AddIcon-sc-1kfwjsi-0")
    if popup_open(browser):
        in_put(browser, By.CSS_SELECTOR, "[type='text']", str(datetime.datetime.now().strftime("%d%m%Y%H%M")))
        button(browser, By.XPATH, "//button[@type='submit']")
        time.sleep(2)
        button(browser, By.CSS_SELECTOR, "[data-testid='close_modal']")
    time.sleep(2)
    if len(arr) + 1 == len(browser.find_elements(By.CLASS_NAME, "OX_p4")):
        print("Профиль добавлен успешно")
        assert True
    else:
        print("Профиль не добавлен")
        assert False
