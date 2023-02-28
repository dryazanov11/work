import time

from selenium.webdriver.common.by import By
import allure

@allure.epic("Страница авторизации")
class TestTMCore():

    def setup(self):

        self.link = "http://r78-test.zdrav.netrika.ru/tm.doctorportal.ui/auth"

    @allure.feature("Корректный ввод данных при авторизации")
    def test_correct_login(self, browser):

        browser.implicitly_wait(5)
        browser.get(self.link)
        browser.set_window_size(1920, 1080)

        #вводим данные регионального админа
        browser.find_element(By.CSS_SELECTOR, "[type='text']").send_keys("reg_admin@test.com")
        browser.find_element(By.CSS_SELECTOR, "[type='password']").send_keys("123")
        browser.find_element(By.CSS_SELECTOR, ".button__primary").click()

        #проверяем что открылся портал находя его иконку
        header = browser.find_element(By.CSS_SELECTOR, ".main-header-logo > div > div:nth-child(1)").text
        assert "Портал ТМК" == header, "Текст в шапке портала не равен ожидаемому"

        #выходим с портала и проверяем что выход успешно удался находя кнопку входа
        browser.find_element(By.CSS_SELECTOR, ".menu-exit > span").click()
        enter_to_portal = browser.find_element(By.CSS_SELECTOR, ".button__primary").text
        assert enter_to_portal == "ВОЙТИ В ЛИЧНЫЙ КАБИНЕТ", "Выход из портала не привел на страницу авторизации"

    @allure.feature("Некорректный ввод данных при авторизации")
    def test_incorrect_login(self, browser):

        browser.implicitly_wait(5)
        browser.get(self.link)
        browser.set_window_size(1920, 1080)

        # вводим некорректные данные
        browser.find_element(By.CSS_SELECTOR, "[type='text']").send_keys("example@example.com")
        browser.find_element(By.CSS_SELECTOR, "[type='password']").send_keys("123")
        browser.find_element(By.CSS_SELECTOR, ".button__primary").click()

        #ждем отображения ошибки и проверяем её текст
        time.sleep(3)
        error_in_login = browser.find_element(By.CSS_SELECTOR, "div.Toastify__toast-body > div:nth-child(2)").text
        assert error_in_login == "Неверный e-mail или пароль", "Ввод некорректных данных не привел к ошибке"

    @allure.feature("Восстановление пароля")
    def test_password_recovery(self, browser):

        browser.implicitly_wait(5)
        browser.get(self.link)
        browser.set_window_size(1920, 1080)

        #переходим к странице восстановления пароля и вводим некорректные данные
        browser.find_element(By.CSS_SELECTOR, ".reset-password-link").click()
        browser.find_element(By.CSS_SELECTOR, ".form-input").send_keys("example@example.com")
        browser.find_element(By.CSS_SELECTOR, ".button__primary").click()

        #проверяем что есть ошибка о ненахождении такого пользователя
        time.sleep(3)
        error_in_recovery = browser.find_element(By.CSS_SELECTOR, "div.Toastify__toast-body > div:nth-child(2)").text
        assert error_in_recovery == "Пользователь не найден", "Ввод некорректного e-mail не привел к ошибке"

        #вводим данные регионального админа и проверяем, что письмо отправляется
        browser.find_element(By.CSS_SELECTOR, ".form-input").clear()
        browser.find_element(By.CSS_SELECTOR, ".form-input").send_keys("reg_admin@test.com")
        browser.find_element(By.CSS_SELECTOR, ".button__primary").click()

        #проверяем, что после отправки письма есть соответствующее сообщение
        time.sleep(3)
        letter_sent = browser.find_element(By.CSS_SELECTOR, ".login-container > div").text
        assert letter_sent == "Письмо отправлено", "Текст об отправке письма не равен ожидаемому"

        #возвращаемся на страницу авторизации
        browser.find_element(By.CSS_SELECTOR, "[href='/tm.doctorportal.ui/auth']").click()
        enter_to_portal = browser.find_element(By.CSS_SELECTOR, ".button__primary").text
        assert enter_to_portal == "ВОЙТИ В ЛИЧНЫЙ КАБИНЕТ", "Выход из портала не привел на страницу авторизации"