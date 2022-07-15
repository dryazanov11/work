import datetime
import time

import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки System")
class TestSystem(BaseCase):

    def setup(self):

        req = "{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО','route':'$.serviceRequest.requesterOrganization','required':true,'parameterType':'value'}"

        self.nokey = "{'referenceName':'Код направляющей МО','route':'$.serviceRequest.requesterOrganization','required':true,'parameterType':'value'}".encode('UTF-8')
        self.noname = "{'referenceKey':'1.2.643.2.69.1.1.1.64','route':'$.serviceRequest.requesterOrganization','required':true,'parameterType':'value'}"
        self.noroute = "{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО','required':true,'parameterType':'value'}".encode('UTF-8')
        self.notype = "{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО','route':'$.serviceRequest.requesterOrganization'}".encode('UTF-8')
        self.dublicate = "{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceName':'Возрастная категория граждан','route':'$.observation.ageType','required':false,'parameterType':'value'}".encode('UTF-8')

        self.create = "{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО','route':'$.serviceRequest.requesterOrganization','required':true,'parameterType':'value'}".encode('UTF-8')
        self.update = "{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО Обновление','required': true, 'route':'$.serviceRequest.requesterOrganization', 'ParameterType': 'value'}".encode('UTF-8')
        self.create_range = "[{'referenceKey':'1.2.643.2.69.1.1.1.148.1','referenceName':'ТМК. Срочность обработки заявки','route':'$.serviceRequest.urgency','required':true,'parameterType':'value'},{'referenceKey':'1.2.643.2.69.1.1.1.64','referenceName':'Код направляющей МО','route':'$.serviceRequest.requesterOrganization','required':false,'parameterType':'value'}]".encode('UTF-8')
        self.expected_fields = ["serviceVersion", "databaseVersion", "buildDate"]

    @allure.feature('Создание конфиги не передавая обязательные параметры')
    def test_create_negative_system(self):

        #без ReferenceKey
        nokey = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.nokey)
        Assertions.assert_json_value_by_name(nokey, 'message', 'Поле ReferenceKey не должно быть пустым', 'Сообщение об ошибке при отсутствии ReferenceKey не равно ожидаемому')

        #без ReferenceName
        noname = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.noname)
        Assertions.assert_json_value_by_name(noname, 'message', 'Поле ReferenceName не должно быть пустым', 'Сообщение об ошибке при отсутствии ReferenceName не равно ожидаемому')

        #без route
        noroute = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.noroute)
        Assertions.assert_json_value_by_name(noroute, 'message', 'Поле Route не должно быть пустым', 'Сообщение об ошибке при отсутствии Route не равно ожидаемому')

        #без ParameterType
        notype = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.notype)
        Assertions.assert_json_value_by_name(notype, 'message', "Поле ParameterType должно иметь значение 'value' или 'range'", 'Сообщение об ошибке при отсутствии ParameterType не равно ожидаемому')

        #передать данные уже существующего конфига
        dublicate = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.dublicate)
        Assertions.assert_json_value_by_name(dublicate, 'message', 'Ссылка на справочник 1.2.643.2.69.1.1.1.223 не уникальна', 'Сообщение об ошибке при дубликате не равно ожидаемому')

    @allure.feature("Передача несуществующего id")
    def test_incorrect_id(self):

        #поиск конфиги по id
        get = MyRequests.get(f'/tm-schedule/api/systems/config/{config.default_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get, 'message', f'Конфигурация с id={config.default_id} не найдена', 'Ошибка при несуществующем ID не равна ожидаемой')

        #обновление конфиги по id
        put = MyRequests.put(f'/tm-schedule/api/systems/config/{config.default_id}',headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                             data=self.notype)
        Assertions.assert_json_value_by_name(put, 'message', f'Конфигурация с id={config.default_id} не найдена', 'Ошибка при несуществующем ID не равна ожидаемой')

        # обновление конфиги по id
        delete = MyRequests.delete(f'/tm-schedule/api/systems/config/{config.default_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', f'Конфигурация с id={config.default_id} не найдена','Ошибка при несуществующем ID не равна ожидаемой')

    @allure.feature("Создание/получение/обновление/удаление конфига")
    def test_create_get_put_delete(self):

        #создание конфига
        create = MyRequests.post('/tm-schedule/api/systems/config', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                data=self.create)
        Assertions.assert_expectedvalue_equal_receivedvalue(create, True, create.json()['result']['required'], 'При создании конфиги получен неожиданный ответ')

        config_id = create.json()['result']['id']

        #запрос на получение созданного ранее конфига
        get = MyRequests.get(f'/tm-schedule/api/systems/config/{config_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, config_id, get.json()['result']['id'], 'При получении конфиги получен неожиданный ответ')

        #обновление названия конфига
        put = MyRequests.put(f'/tm-schedule/api/systems/config/{config_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                             data=self.update)
        Assertions.assert_expectedvalue_equal_receivedvalue(put, 'Код направляющей МО Обновление', put.json()['result']['referenceName'], 'При обновлении конфиги получен неожиданный ответ')

        #удаление конфиги
        delete = MyRequests.delete(f'/tm-schedule/api/systems/config/{config_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление прошло неуспешно')

        #проверяю удаленный конфиг
        get_deleted = MyRequests.get(f'/tm-schedule/api/systems/config/{config_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get_deleted, 'message', f'Конфигурация с id={config_id} не найдена', 'Удаленный конфиг остался в системе')

    @allure.feature("Проверка что методы поиска рабочие + предзаполнение данных systemConfig")
    def test_search_createrange(self):

        create_range = MyRequests.post('/tm-schedule/api/systems/config/createRange', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                               data=self.create_range)
        Assertions.assert_json_value_by_name(create_range, 'success', True, 'Предзаполнение конфиг вышло неудачным или такие конфиги уже заведены')

        #ищу id созданных конфиг
        search = MyRequests.get('/tm-schedule/api/systems/config?pageSize=10', headers={'Authorization': f'{config.token_test_schedule}'})
        configs = search.json()['result']['items']

        #создаю пустой список, чтобы внести в него значения конфиг
        list_of_createrange = []

        #перебираю конфиги из ответа get метода по названию и вношу их в пустой список
        for i in range(len(configs)):
            if configs[i]['referenceName'] == 'ТМК. Срочность обработки заявки' or configs[i]['referenceName'] == 'Код направляющей МО':
                list_of_createrange.append(configs[i]['id'])
            if configs[i]['referenceName'] == 'ТМК. Срочность обработки заявки':
                required_id = configs[i]['id']

                #проверка что он будет в ответе метода поиска обязательных конфиг
                search_required = MyRequests.get('/tm-schedule/api/systems/config/required?pageIndex=1&pageSize=10', headers={'Authorization': f'{config.token_test_schedule}'})
                Assertions.assert_expectedvalue_equal_receivedvalue(search_required, required_id, search_required.json()['result']['items'][0]['id'],
                                                                    'Метод поиска обязательных конфиг содержит в ответе не ожидаемую информацию')

        id_1 = list_of_createrange[0]
        id_2 = list_of_createrange[1]

        #проверяю что найдены были два конфига, которые были созданы заранее
        Assertions.assert_value_equeals_expected(len(list_of_createrange), 2)

        #удаляю их
        delete_1 = MyRequests.delete(f'/tm-schedule/api/systems/config/{id_1}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete_1, 'success', True, 'Удаление прошло неуспешно')

        delete_2 = MyRequests.delete(f'/tm-schedule/api/systems/config/{id_2}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete_2, 'success', True, 'Удаление прошло неуспешно')

        #проверка получения постраничного списка маршрутов
        getworkflows = MyRequests.get('/tm-schedule/api/tmCore/getWorkflows?name=QA-plugins&isDisabled=false', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(getworkflows, '09872eef-6180-4f5f-9137-c33ce60ad416', getworkflows.json()['result']['items'][0]['id'], 'Полученный id не равен ожидаемому')

        api = MyRequests.get('/tm-schedule/api/_version')
        Assertions.assert_json_has_keys(api, self.expected_fields)