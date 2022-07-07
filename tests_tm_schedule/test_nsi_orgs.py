import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки NSI")
class TestNsi(BaseCase):

    def setup(self):
        self.request_orgs = "{'filter':[{'referenceKey':'1.2.643.5.1.13.13.11.1070','referenceCode':'B01.064.003'}]}"

    @allure.feature("Вызовы GET методов в НСИ")
    def test_search_nsi(self):

        #поиск записи о специалисте в НСИ
        practitioner = MyRequests.get(f'/tm-schedule/api/nsi/practitioner/_search?snils={config.snils}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(practitioner, 'success', True, 'Данные о враче не вернулись')
        Assertions.assert_expectedvalue_equal_receivedvalue(practitioner, 'Петренко', practitioner.json()['result']['lastName'], 'В ответе пришел иной врач')

        #поиск записи о специалисте в НСИ (административный метод)
        practitioner_admin = MyRequests.get(f'/tm-schedule/api/nsi/practitioner/admin/_search?snils={config.snils_admin}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(practitioner_admin, 'success', True, 'Данные о враче не вернулись')
        Assertions.assert_expectedvalue_equal_receivedvalue(practitioner_admin, 'Морозова',practitioner_admin.json()['result']['lastName'], 'В ответе пришел иной врач')

        #получение списка справочников НСИ
        dictionaries = MyRequests.get('/tm-schedule/api/nsi/dictionaries', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(dictionaries, 'success', True, 'Данные о справочниках не вернулись')

        #получение списка значений справочника НСИ
        dictionaryvalues = MyRequests.get('/tm-schedule/api/nsi/dictionaryValues?oid=1.2.643.2.69.1.1.1.223', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(dictionaryvalues, 'success', True, 'Данные о значениях справочника не вернулись')

        #проверка получения поля Name для указанного значения справочника
        lookupNameAsync = MyRequests.get('/tm-schedule/api/nsi/lookupNameAsync?code=1&uri=1.2.643.2.69.1.1.1.223', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(lookupNameAsync, 'дети', lookupNameAsync.text, 'В ответе пришло неожидаемое значение')

    @allure.feature("Поиск уникальных организаций по заданным фильтрам атрибутов их профилей")
    def test_search_orgs(self):

        orgs = MyRequests.post('/tm-schedule/api/organizations/byAttributes', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                               data=self.request_orgs)
        Assertions.assert_expectedvalue_equal_receivedvalue(orgs, '91593c1f-c130-4312-9a97-8c017de6a1de', orgs.json()['result'][0]['id'], 'Полученный id МО отличается от ожидаемого')