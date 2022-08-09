import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Commands")
class TestValidator(BaseCase):
    def setup(self):

        self.noname_validator = "{'messageOnError':'Message','areaId':'cbad64d2-eb21-4c4f-9ea3-243c26f7fca2','schemaId':'c4100298-c735-48cb-996f-a8f43a1aa646','expression':'true'}"
        self.nomessage_error_validator = "{'name':'name','areaId':'cbad64d2-eb21-4c4f-9ea3-243c26f7fca2','schemaId':'c4100298-c735-48cb-996f-a8f43a1aa646','expression':'true'}"
        self.noarea_validator = "{'name':'name','messageOnError':'Message','schemaId':'c4100298-c735-48cb-996f-a8f43a1aa646','expression':'true'}"
        self.expression_validator = "{'name':'name','messageOnError':'Message','schemaId':'c4100298-c735-48cb-996f-a8f43a1aa646','areaId':'cbad64d2-eb21-4c4f-9ea3-243c26f7fca2'}"

        self.create_validator = "{\"Name\":\"autocheck\",\"Expression\":\"('{$$system}' = 'N3 1a55e61b-dd7a-4acf-a94a-37d21d761af5')\",\"MessageOnError\":\"test_error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\",\"SchemaId\":\"c4100298-c735-48cb-996f-a8f43a1aa646\"}"
        self.create_dublicate_name_validator = "{\"Name\":\"Autotest Check\",\"Expression\":\"('{$$system}' = 'N3 1a55e61b-dd7a-4acf-a94a-37d21d761af5')\",\"MessageOnError\":\"test_error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\",\"SchemaId\":\"c4100298-c735-48cb-996f-a8f43a1aa646\"}"

    @allure.feature("Негативные тесты на внутренний валидатор")
    def test_negative_validator(self):

        #создание валидатора без name
        noname = MyRequests.post('/tm-core/api/Commands/RegisterValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.noname_validator)
        Assertions.assert_json_value_by_name(noname, 'message', "validatorName is required parameter", 'Неожиданная ошибка при создании внутреннего валидатора без name')

        #без messageOnError
        nomessage_error = MyRequests.post('/tm-core/api/Commands/RegisterValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                          data=self.nomessage_error_validator)
        Assertions.assert_json_value_by_name(nomessage_error, 'message', "Value cannot be null.\nParameter name: messageOnError",
                                             'Неожиданная ошибка при создании внутреннего валидатора без messageOnError')

        #нет areaId - ЗАВЕДЕНА ЗАДАЧА https://jira.netrika.ru/browse/TELEMED-2133
        noarea = MyRequests.post('/tm-core/api/Commands/RegisterValidator',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_tm_core}'},
                                       data=self.noarea_validator)
        Assertions.assert_json_value_by_name(noarea, 'message', "23503: INSERT или UPDATE в таблице \"validator\" нарушает ограничение внешнего ключа \"area_id\"",
                                             'Неожиданная ошибка при создании внутреннего валидатора без area_id')

        #нет expression
        noexpression = MyRequests.post('/tm-core/api/Commands/RegisterValidator',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_tm_core}'},
                                       data=self.expression_validator)
        Assertions.assert_json_value_by_name(noexpression, 'message', "Value cannot be null.\nParameter name: expression",'Неожиданная ошибка при создании внутреннего валидатора без expression')

        #проверка дубликата имени
        dublicate = MyRequests.post('/tm-core/api/Commands/RegisterValidator',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_tm_core}'},
                                       data=self.create_dublicate_name_validator)
        Assertions.assert_json_value_by_name(dublicate, 'message', 'Duplicate validator name', 'При дубликате имени валидатора получена неожидаемая ошибка')

        #обновление с несуществующим id - https://jira.netrika.ru/browse/TELEMED-2133

        #получение несуществующего id
        get_validator = MyRequests.get(f'/tm-core/api/Queries/GetValidator/{config.default_id}',headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(get_validator, 'message', f"Validator '{config.default_id}' not found",'Неожиданное сообщение об ошибке')

        #удаление несуществующего id - https://jira.netrika.ru/browse/TELEMED-2133

    @allure.feature("Создание/получение/обновление/удаление валидатора")
    def test_create_update_get_delete_validator(self):

        #создание внутреннего валидатора
        create = MyRequests.post('/tm-core/api/Commands/RegisterValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                          data=self.create_validator)
        validator_id = create.json()['result']['id']

        replace_values = {'autocheck': 'name_autotest_update', 'test_error': 'test_error_update'}
        self.create_validator = self.multiple_replace(self.create_validator, replace_values)

        update = MyRequests.post(f'/tm-core/api/Commands/UpdateValidator/{validator_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.create_validator)
        Assertions.assert_expectedvalue_equal_receivedvalue(update, 'name_autotest_update', update.json()['result']['name'], 'Name после обновления не соответствует ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(update, 'test_error_update', update.json()['result']['messageOnError'], 'messageOnError после обновления не соответствует ожидаемому')

        get = MyRequests.get(f'/tm-core/api/Queries/GetValidator/{validator_id}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, validator_id, get.json()['result']['id'], 'Информация, полученная в ответе не соответствует запрошенному ID валидатора')

        delete = MyRequests.delete(f'/tm-core/api/Commands/DeleteValidator/{validator_id}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление внешнего валидатора прошло неуспешно')

        get_all = MyRequests.get('/tm-core/api/Queries/GetValidators?take=100', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(get_all, 'success', True, 'Метод получения всех валидаторов ответил неуспешно')

@allure.epic("Полноценные проверки Commands")
class TestExternalValidator(BaseCase):

    def setup(self):
        self.create_exvalidator = "{\"Name\":\"autotest\",\"Url\":\"http://r78-test.zdrav.netrika.ru/tm-schedule/api/profiles/available\",\"MessageOnError\":\"message_about_error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\"}"

        self.no_name_exvalidator = "{\"Url\":\"http://r78-test.zdrav.netrika.ru/tm-schedule/api/profiles/available\",\"MessageOnError\":\"message about error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\"}"
        self.no_url_exvalidator = "{\"Name\":\"autotest\",\"MessageOnError\":\"message about error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\"}"
        self.no_message_exvalidator = "{\"Name\":\"autotest\",\"Url\":\"http://r78-test.zdrav.netrika.ru/tm-schedule/api/profiles/available\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\"}"
        self.no_area_exvalidator = "{\"Name\":\"autotest\",\"Url\":\"http://r78-test.zdrav.netrika.ru/tm-schedule/api/profiles/available\",\"MessageOnError\":\"message about error\"}"
        self.dublicate_name_exvalidator = "{\"Name\":\"Autocheck\",\"Url\":\"http://r78-test.zdrav.netrika.ru/tm-schedule/api/profiles/available\",\"MessageOnError\":\"message about error\",\"AreaId\":\"cbad64d2-eb21-4c4f-9ea3-243c26f7fca2\"}"

    @allure.feature("Негативные тесты на внешний валидатор")
    def test_negative_externalvalidator(self):

        #создание внешнего валидатора без name
        noname = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.no_name_exvalidator)
        Assertions.assert_json_value_by_name(noname, 'message', 'validatorName is required parameter', 'Неожиданная ошибка при создании внутреннего валидатора без name')

        #не передан url - https://jira.netrika.ru/browse/TELEMED-2133
        nourl = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.no_url_exvalidator)
        Assertions.assert_json_value_by_name(nourl, 'message', "Value cannot be null.\nParameter name: url", 'Неожиданная ошибка при создании внутреннего валидатора без url')

        #не передан MessageOnError - https://jira.netrika.ru/browse/TELEMED-2133
        nomessage = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.no_message_exvalidator)
        Assertions.assert_json_value_by_name(nomessage, 'message', "Value cannot be null.\nParameter name: messageOnError", 'Неожиданная ошибка при создании внутреннего валидатора без messageOnError')

        #не передан areaid - https://jira.netrika.ru/browse/TELEMED-2133
        noarea = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.no_area_exvalidator)
        Assertions.assert_json_value_by_name(noarea, 'message', "23503: INSERT или UPDATE в таблице \"validator\" нарушает ограничение внешнего ключа \"area_id\"",
                                             'Неожиданная ошибка при создании внутреннего валидатора без area_id')

        #дубликат имени
        dublicate = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.dublicate_name_exvalidator)
        Assertions.assert_json_value_by_name(dublicate, 'message', "Duplicate validator name", 'Неожиданная ошибка при дубликате имени')

        #обновление с несуществующим id - https://jira.netrika.ru/browse/TELEMED-2133

    @allure.feature("Создание/получение/обновление/удаление внешнего валидатора")
    def test_create_update_get_delete_validator(self):

        create = MyRequests.post('/tm-core/api/Commands/RegisterExternalValidator', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.create_exvalidator)
        validator_id = create.json()['result']['id']

        replace_values = {'autotest': 'name_autotest_update', 'message_about_error': 'test_error_update'}
        self.create_exvalidator = self.multiple_replace(self.create_exvalidator, replace_values)

        update = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/{validator_id}',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_tm_core}'},
                                 data=self.create_exvalidator)
        Assertions.assert_expectedvalue_equal_receivedvalue(update, 'name_autotest_update',update.json()['result']['name'],'Name после обновления не соответствует ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(update, 'test_error_update',update.json()['result']['messageOnError'],'messageOnError после обновления не соответствует ожидаемому')

        get = MyRequests.get(f'/tm-core/api/Queries/GetValidator/{validator_id}',headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, validator_id, get.json()['result']['id'],'Информация, полученная в ответе не соответствует запрошенному ID валидатора')

        delete = MyRequests.delete(f'/tm-core/api/Commands/DeleteValidator/{validator_id}',headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление внешнего валидатора прошло неуспешно')


@allure.epic("Полноценные проверки Commands")
class TestCallback(BaseCase):

    def setup(self):

        self.create_callback = "{'Name':'Autocheck','Url':'http://r78-test.zdrav.netrika.ru/tm-plugins/Callbacks/TryChangeState'}"
        self.noname = "{'Url':'http://r78-test.zdrav.netrika.ru/tm-plugins/Callbacks/TryChangeState'}"
        self.nourl = "{'Name':'autotest'}"

        self.update_name = "{'Name':'update from autotest'}"

    @allure.feature("Негативные тесты на Callback")
    def test_negative_callback(self):

        #без name
        noname = MyRequests.post('/tm-core/api/Commands/RegisterCallback', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},data=self.noname)
        Assertions.assert_json_value_by_name(noname, 'message', 'callbackName is required parameter', 'Неожиданная ошибка при создании callback без name')

        #без url - https://jira.netrika.ru/browse/TELEMED-2133
        nourl = MyRequests.post('/tm-core/api/Commands/RegisterCallback',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_tm_core}'},data=self.nourl)
        Assertions.assert_json_value_by_name(nourl, 'message', 'Value cannot be null.\nParameter name: url','Неожиданная ошибка при создании callback без url')

        #дубликат названия
        dublicate = MyRequests.post('/tm-core/api/Commands/RegisterCallback', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},data=self.create_callback)
        Assertions.assert_json_value_by_name(dublicate, 'message', 'Duplicate callback name', 'Неожиданная ошибка при создании callback с дублем name')

        #обновление с несуществующим id - https://jira.netrika.ru/browse/TELEMED-2133
        incorrect_update = MyRequests.post(f'/tm-core/api/Commands/UpdateCallback/{config.default_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},data="{}")
        Assertions.assert_json_value_by_name(incorrect_update, 'message', f'Callback with id ${config.default_id} not found', 'Неожиданная ошибка при обновлении callback с несуществующим ID')

        #удаление с несуществующим id - https://jira.netrika.ru/browse/TELEMED-2133
        incorrect_delete = MyRequests.delete(f'/tm-core/api/Commands/DeleteCallback/{config.default_id}',headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(incorrect_delete, 'message',f'Callback with id ${config.default_id} not found','Неожиданная ошибка при удалении callback с несуществующим ID')

        #поиск несуществующего callback
        incorrect_get = MyRequests.get(f'/tm-core/api/Queries/GetCallback/{config.default_id}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(incorrect_get, 'message', f"Callback '{config.default_id}' not found", 'Неожиданная ошибка при обновлении callback с несуществующим ID')

    @allure.feature("Создание/получение/обновление/удаление коллбэка")
    def test_create_update_get_delete_callback(self):

        self.create_callback = self.create_callback.replace('Autocheck', 'autotest')
        create = MyRequests.post('/tm-core/api/Commands/RegisterCallback', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},data=self.create_callback)
        Assertions.assert_json_value_by_name(create, 'success', True, 'Неожиданная ошибка при создании callback')

        callback_id = create.json()['result']['id']

        update = MyRequests.post(f'/tm-core/api/Commands/UpdateCallback/{callback_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_tm_core}'},
                                 data=self.update_name)
        Assertions.assert_expectedvalue_equal_receivedvalue(update, update.json()['result']['name'], 'update from autotest', 'Неожиданная ошибка при обновлении callback')

        get = MyRequests.get(f'/tm-core/api/Queries/GetCallback/{callback_id}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(get, 'success', True, 'Неожиданная ошибка при получении callback')

        get_all = MyRequests.get('/tm-core/api/Queries/GetCallbacks', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(get_all, 'success', True, 'Неожиданная ошибка при получении callback')

        delete = MyRequests.delete(f'/tm-core/api/Commands/DeleteCallback/{callback_id}',headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_json_value_by_name(delete, 'success',True,'Неожиданная ошибка при удалении callback')