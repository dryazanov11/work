import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Report")
class TestReport(BaseCase):
    def setup(self):

        self.noname = "{\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"
        self.nolink = "{\"name\": \"Autocheck\",\"type\": \"QA-area\"}"
        self.notype = "{\"link\": \"bfe35b34-2824-4af6-95c9-49965998f081\", \"name\": \"Autocheck\"}"
        self.dublicate = "{\"name\":\"QA-test\",\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"
        self.wrong_data = "{\"name\":\"test\",\"link\":\"50752145-1d1b-42cc-b052-2892a84485ed\",\"type\":\"test\"}"

        self.create = "{\"name\":\"autotest\",\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"

    @allure.feature("Негативные тесты на отчёт")
    def test_negative_report(self):

        #создание без name
        noname = MyRequests.post('/tm_reports/api/Report', headers={'Content-Type': 'application/json'}, data=self.noname)
        Assertions.assert_json_value_by_name(noname, 'Message', "Name - обязательный параметр.", noname.json()['Message'])

        #создание без link
        nolink = MyRequests.post('/tm_reports/api/Report', headers={'Content-Type': 'application/json'},data=self.nolink)
        Assertions.assert_json_value_by_name(nolink, 'Message', "Link - обязательный параметр.",nolink.json()['Message'])

        #создание без type
        notype = MyRequests.post('/tm_reports/api/Report', headers={'Content-Type': 'application/json'},data=self.notype)
        Assertions.assert_json_value_by_name(notype, 'Message', "Type - обязательный параметр.",notype.json()['Message'])

        #создание с дублем name
        dublicate = MyRequests.post('/tm_reports/api/Report', headers={'Content-Type': 'application/json'}, data=self.dublicate)
        Assertions.assert_json_value_by_name(dublicate, 'Message', "Отчет с таким name = 'QA-test' или внешним идентификатором сущности = 'bfe35b34-2824-4af6-95c9-49965998f081' уже существует.",
                                             dublicate.json()['Message'])

        #обновление с несуществующим id
        update_with_incorrect_id = MyRequests.put(f'/tm_reports/api/Report/{config.default_id}', headers={'Content-Type': 'application/json'}, data=self.wrong_data)
        Assertions.assert_json_value_by_name(update_with_incorrect_id, 'Message', f"Отчет с id = '{config.default_id}' не найден.", update_with_incorrect_id.json()['Message'])

        #получение несуществующего id
        get_incorrect_id = MyRequests.get(f'/tm_reports/api/Report/{config.default_id}')
        Assertions.assert_json_value_by_name(get_incorrect_id, 'Message', f"Отчет с id = '{config.default_id}' не найден.", get_incorrect_id.json()['Message'])

        #удаление несуществующего id
        delete_incorrect_id = MyRequests.delete(f'/tm_reports/api/Report/{config.default_id}')
        Assertions.assert_json_value_by_name(delete_incorrect_id, 'Message', f"Отчет с id = '{config.default_id}' не найден.", delete_incorrect_id.json()['Message'])

    @allure.feature("CRUD отчёта")
    def test_crud_report(self):

        create = MyRequests.post('/tm_reports/api/Report', headers={'Content-Type': 'application/json'},data=self.create)
        Assertions.assert_json_value_by_name(create, 'name', 'autotest', 'Создание отчёта привело к ошибке')

        reportId = create.json()['id']

        get = MyRequests.get(f'/tm_reports/api/Report/{reportId}')
        Assertions.assert_json_value_by_name(get, 'name', 'autotest', 'Получение отчёта закончилось неудачей')

        self.create = self.create.replace('autotest', 'autotest update')

        update = MyRequests.put(f'/tm_reports/api/Report/{reportId}', headers={'Content-Type': 'application/json'}, data=self.create)
        Assertions.assert_json_value_by_name(update, 'name', "autotest update", 'Обновление отчёта привело к ошибке')

        delete = MyRequests.delete(f'/tm_reports/api/Report/{reportId}')
        Assertions.assert_body(delete, f'Отчет {reportId} удален.')

    #@allure.feature("Проверка методов получения отчётов, построения файлов") - добраться как получится настроить данные на тесте внутри отчёта
