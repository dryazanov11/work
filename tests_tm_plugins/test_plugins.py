import datetime
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Проверки Plugins")
class TestPresenceParameterValueValidator(BaseCase):

    def setup(self):

        self.snp_check_value_for_nsi = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check NSI","InitialTransitionId":"6ce8ec25-c09b-4bf1-81a9-541f749bac7c","ProcessContext":{"lpu":{"idLpu":"test_value"}},"roleContext":{}}'
        self.snp_check_value_for_nsi_array = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check NSI","InitialTransitionId":"6ce8ec25-c09b-4bf1-81a9-541f749bac7c","ProcessContext":{"arrayLpu":[{"id":"1","idLpu":"test_array_value","isDeleted":false}]},"roleContext":{}}'

        self.mts_check_value_for_nsi = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"lpu":{"idLpu":"test_value"}},"roleContext":{}}'
        self.mts_check_value_for_nsi_array = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"arrayLpu":[{"id":"1","idLpu":"test_array_value","isDeleted":false}]},"roleContext":{}}'

        self.mts_check_empty_for_nsi = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"lpu":{"idLpu":""}},"roleContext":{}}'
        self.mts_check_empty_for_nsi_array = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"arrayLpu":[{"id":"1","idLpu":"","isDeleted":false}]},"roleContext":{}}'

        self.last_stage_id = 'a22cfdd7-6a54-4ed2-9b49-6d527afae3d1'

    @allure.feature("Тесты на плагин, который проверяет что значение есть в НСИ")
    def testPresenceParameterValueValidator(self):

        #проверка при передаче неверного значения при создании
        incorrect_value_snp = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.snp_check_value_for_nsi)
        Assertions.assert_json_value_by_name(incorrect_value_snp, 'message', "The code 'test_value' with JSON context path 'lpu.idLpu' is missing in the directory with the Oid '1.2.643.2.69.1.1.1.64' with oids parameter JSON context schema path 'properties.lpu.properties.idLpu' ",
                                             "Получен неожиданный результат в результате передачи неверного значения для НСИ")

        incorrect_value_snp_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.snp_check_value_for_nsi_array)
        Assertions.assert_json_value_by_name(incorrect_value_snp_array, 'message', "The code 'test_array_value' with JSON context path 'arrayLpu[0].idLpu' is missing in the directory with the Oid '1.2.643.2.69.1.1.1.64' with oids parameter JSON context schema path 'properties.arrayLpu.items.properties.idLpu' ",
                                             "Получен неожиданный результат в результате передачи неверного значения для НСИ")

        #передача верного значения из справочника при создании
        self.snp_check_value_for_nsi = self.snp_check_value_for_nsi.replace('test_value', config.idLpu)
        create = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.snp_check_value_for_nsi)
        Assertions.assert_json_value_by_name(create, 'success', True, 'Направление не удалось создать')
        processId = create.json()['processId']

        self.snp_check_value_for_nsi_array = self.snp_check_value_for_nsi_array.replace('test_array_value', config.idLpu)
        create_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.snp_check_value_for_nsi_array)
        Assertions.assert_json_value_by_name(create_array, 'success', True, 'Направление не удалось создать')
        processIdArray = create_array.json()['processId']

        #проверка при передаче пустого значения при создании
        self.snp_check_value_for_nsi = self.snp_check_value_for_nsi.replace(config.idLpu, '')
        empty_value_snp = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.snp_check_value_for_nsi)
        Assertions.assert_json_value_by_name(empty_value_snp, 'message', "The reference code was not found in the 'context' variable.  Oid =>'1.2.643.2.69.1.1.1.64', OidParameterPath => 'properties.lpu.properties.idLpu', CodeKey => 'idLpu', CodeKeyPath => 'lpu.idLpu', CodeValue => '' ",
                                             "Получен неожиданный результат в результате передачи пустого значения для НСИ")

        self.snp_check_value_for_nsi_array = self.snp_check_value_for_nsi_array.replace(config.idLpu, '')
        empty_value_snp_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.snp_check_value_for_nsi_array)
        Assertions.assert_json_value_by_name(empty_value_snp_array, 'message',"The reference code was not found in the 'context' variable.  Oid =>'1.2.643.2.69.1.1.1.64', OidParameterPath => 'properties.arrayLpu.items.properties.idLpu', CodeKey => 'idLpu', CodeKeyPath => 'arrayLpu[0].idLpu', CodeValue => '' ",
                                             "Получен неожиданный результат в результате передачи пустого значения для НСИ")

        self.mts_check_value_for_nsi = self.mts_check_value_for_nsi.replace('example', processId)
        self.mts_check_value_for_nsi_array = self.mts_check_value_for_nsi_array.replace('example', processIdArray)

        #проверка при передаче неверного значения при смене статуса
        incorrect_value_mts = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.mts_check_value_for_nsi)
        Assertions.assert_json_value_by_name(incorrect_value_mts, 'message', "The code 'test_value' with JSON context path 'lpu.idLpu' is missing in the directory with the Oid '1.2.643.2.69.1.1.1.64' with oids parameter JSON context schema path 'properties.lpu.properties.idLpu' ",
                                             'Получен неожиданный результат в результате передачи неверного значения для НСИ')

        incorrect_value_mts_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.mts_check_value_for_nsi_array)
        Assertions.assert_json_value_by_name(incorrect_value_mts_array, 'message', "The code 'test_array_value' with JSON context path 'arrayLpu[0].idLpu' is missing in the directory with the Oid '1.2.643.2.69.1.1.1.64' with oids parameter JSON context schema path 'properties.arrayLpu.items.properties.idLpu' ",
                                             'Получен неожиданный результат в результате передачи неверного значения для НСИ')

        self.mts_check_empty_for_nsi = self.mts_check_empty_for_nsi.replace('example', processId)
        self.mts_check_empty_for_nsi_array = self.mts_check_empty_for_nsi_array.replace('example', processIdArray)

        #проверка при передаче пустого значения при смене статуса
        empty_value_mts = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.mts_check_empty_for_nsi)
        Assertions.assert_json_value_by_name(empty_value_mts, 'message', "The reference code was not found in the 'context' variable.  Oid =>'1.2.643.2.69.1.1.1.64', OidParameterPath => 'properties.lpu.properties.idLpu', CodeKey => 'idLpu', CodeKeyPath => 'lpu.idLpu', CodeValue => '' ",
                                             'Получен неожиданный результат в результате передачи пустого значения для НСИ')

        empty_value_mts_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.mts_check_empty_for_nsi_array)
        Assertions.assert_json_value_by_name(empty_value_mts_array, 'message', "The reference code was not found in the 'context' variable.  Oid =>'1.2.643.2.69.1.1.1.64', OidParameterPath => 'properties.arrayLpu.items.properties.idLpu', CodeKey => 'idLpu', CodeKeyPath => 'arrayLpu[0].idLpu', CodeValue => '' ",
                                             'Получен неожиданный результат в результате передачи пустого значения для НСИ')

        #передача верного значения из справочника при смене статуса
        self.mts_check_value_for_nsi = self.mts_check_value_for_nsi.replace('test_value', config.idLpu)
        move = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.mts_check_value_for_nsi)
        Assertions.assert_json_value_by_name(move, 'success', True, 'Смена статуса завершена неуспешно')

        self.mts_check_value_for_nsi_array = self.mts_check_value_for_nsi_array.replace('test_array_value',config.idLpu)
        move_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                       data=self.mts_check_value_for_nsi_array)
        Assertions.assert_json_value_by_name(move_array, 'success', True, 'Смена статуса завершена неуспешно')

        #проверка что оба направления в статусе 2
        check_status = MyRequests.get(f'/tm-core/api/Queries/GetProcess/{processId}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(check_status, check_status.json()['result']['currentStageId'],
                                                            self.last_stage_id, 'Полученный статус направления не равен ожидаемому')

        check_status_array = MyRequests.get(f'/tm-core/api/Queries/GetProcess/{processIdArray}', headers={'Authorization': f'{config.token_tm_core}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(check_status_array,check_status_array.json()['result']['currentStageId'],
                                                            self.last_stage_id,'Полученный статус направления не равен ожидаемому')

@allure.epic("Проверки Plugins")
class TestRequiredValue(BaseCase):

    def setup(self):

        self.snp_check_req = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.mts_check_req = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'

        self.snp_no_values_from_object = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"lpu":{},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.snp_no_object = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.snp_no_array = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"}},"roleContext":{}}'
        self.snp_no_value_in_array = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]},"roleContext":{}}'

        self.mts_no_values_from_object = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.mts_no_object = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.mts_no_array = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"}},"roleContext":{}}'
        self.mts_no_value_in_array = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{"address":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682"},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]},"roleContext":{}}'

    @allure.feature("Тесты на обязательность параметра")
    def testRequiredValue(self):

        #не передать при создании параметры объекта
        snp_no_values_in_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.snp_no_values_from_object)
        Assertions.assert_json_value_by_name(snp_no_values_in_object, 'message', "Следующие поля отсутствуют или не заполнены: Идентификатор МО, Адрес МО\nDetails:\n[#/lpu/idLpu] - Поле не заполнено или отсутствует\n[#/lpu/address] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать объект при создании
        snp_no_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.snp_no_object)
        Assertions.assert_json_value_by_name(snp_no_object, 'message', "Следующие поля отсутствуют или не заполнены: Объект МО\nDetails:\n[#/lpu] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать массив при создании
        snp_no_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.snp_no_array)
        Assertions.assert_json_value_by_name(snp_no_array, 'message',"Следующие поля отсутствуют или не заполнены: Массив МО\nDetails:\n[#/arrayLpu] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать при создании значение из второго элемента массива
        snp_no_value_in_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.snp_no_value_in_array)
        #текст ошибки решено не править, т.к. обещает большие трудозатраты
        Assertions.assert_json_value_by_name(snp_no_value_in_array, 'message','Object reference not set to an instance of an object.',
                                             'Получена неожиданная ошибка')

        #проверка, что направление успешно создается при переданных обязательных параметрах
        create = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.snp_check_req)

        processId = create.json()['processId']
        self.mts_check_req = self.mts_check_req.replace('example', processId)

        #не передать в movetostage параметры объекта
        self.mts_no_values_from_object = self.mts_no_values_from_object.replace('example', processId)
        mts_no_values_from_object = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.mts_no_values_from_object)
        Assertions.assert_json_value_by_name(mts_no_values_from_object, 'message', "Следующие поля отсутствуют или не заполнены: Идентификатор МО, Адрес МО\nDetails:\n[#/lpu/idLpu] - Поле не заполнено или отсутствует\n[#/lpu/address] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать объект при смене статуса
        self.mts_no_object = self.mts_no_object.replace('example', processId)
        mts_no_object = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_object)
        Assertions.assert_json_value_by_name(mts_no_object, 'message',"Следующие поля отсутствуют или не заполнены: Объект МО\nDetails:\n[#/lpu] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать массив при смене статуса
        self.mts_no_array = self.mts_no_array.replace('example', processId)
        mts_no_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_array)
        Assertions.assert_json_value_by_name(mts_no_array, 'message',"Следующие поля отсутствуют или не заполнены: Массив МО\nDetails:\n[#/arrayLpu] - Поле не заполнено или отсутствует",
                                             'Получена неожиданная ошибка')

        #не передать значение из 2 элемента массива в movetostage
        self.mts_no_value_in_array = self.mts_no_value_in_array.replace('example', processId)
        mts_no_value_in_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_value_in_array)
        # текст ошибки решено не править, т.к. обещает большие трудозатраты
        Assertions.assert_json_value_by_name(mts_no_value_in_array, 'message','Object reference not set to an instance of an object.',
                                             'Получена неожиданная ошибка')

        #проверка что статус успешно меняется
        move = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.mts_check_req)
        Assertions.assert_json_value_by_name(move, 'success', True, 'Смена статуса закончилась неудачей')

@allure.epic("Проверки Plugins")
class TestActiveProfile(BaseCase):

    def setup(self):

        self.inactive = "0384de2e-8ed4-48e5-9088-5542e31ea956"
        self.active = "4dd59db4-a3ac-4ad9-b5a6-c8d223fd1975"
        self.create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_required','InitialTransitionId':'290ca2fd-5c48-4298-a095-797c3f019ca5','ProcessContext':{'profile':{'id':'test_value'},'serviceRequest':{'category':'100'}},'roleContext':{}}"

        self.move = "{'processId':'example','transitionId':'e31b28c1-f191-408b-bbd3-88548cd4cc5a','processContext':{'profile':{'id':'test_value'},'serviceRequest':{'category':'100'}},'roleContext':{}}"

    @allure.feature("Тесты на активность профиля")
    def testProfile(self):

        #несуществующий профиль при создании
        self.create = self.create.replace('test_value', config.default_id)
        create_incorrect_id = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.create)
        Assertions.assert_json_value_by_name(create_incorrect_id, 'message', 'Не удалось найти профиль с указанным ID', 'Получена неожиданная ошибка при некорректном ID профиля')

        #неактивный профиль при создании
        self.create = self.create.replace(config.default_id, self.inactive)
        create_inactive_id = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.create)
        Assertions.assert_json_value_by_name(create_inactive_id, 'message', 'Указанный профиль неактивен', 'Получена неожиданная ошибка при неактивном ID профиля')

        #активный профиль при создании
        self.create = self.create.replace(self.inactive, self.active)
        create_active_id = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.create)
        Assertions.assert_json_value_by_name(create_active_id, 'success', True, 'Получена неожиданная ошибка при активном ID профиля')

        processId = create_active_id.json()['processId']
        self.move = self.move.replace('example', processId)

        #несуществующий профиль при смене статуса
        self.move = self.move.replace('test_value', config.default_id)
        move_incorrect_id = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.move)
        Assertions.assert_json_value_by_name(move_incorrect_id, 'message', 'Не удалось найти профиль с указанным ID', 'Получена неожиданная ошибка при некорректном ID профиля')

        #неактивный профиль при смене статуса
        self.move = self.move.replace(config.default_id, self.inactive)
        move_inactive_id = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.move)
        Assertions.assert_json_value_by_name(move_inactive_id, 'message', 'Указанный профиль неактивен', 'Получена неожиданная ошибка при неактивном ID профиля')

        #активный профиль при смене статуса
        self.move = self.move.replace(self.inactive, self.active)
        move_active_id = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                       data=self.move)
        Assertions.assert_json_value_by_name(move_active_id, 'success', True, 'Получена неожиданная ошибка при активном ID профиля')

@allure.epic("Проверки Plugins")
class TestStringParameter(BaseCase):

    def setup(self):

        self.success_create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'41ae58e2-0dfd-4e55-9c65-a24a9cc2ada1','ProcessContext':{'lpu':{'address':'test_value_object'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'test_value_array','isDeleted':false}]},'roleContext':{}}"
        self.create_incorrect_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'41ae58e2-0dfd-4e55-9c65-a24a9cc2ada1','ProcessContext':{'lpu':{'address':1},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'test_value_array','isDeleted':false}]},'roleContext':{}}"
        self.create_incorrect_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'41ae58e2-0dfd-4e55-9c65-a24a9cc2ada1','ProcessContext':{'lpu':{'address':'test_value_object'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]},'roleContext':{}}"

        self.success_move = "{'processId':'example','transitionId':'c7c16b5c-75fa-4fc5-8912-cbf4af72fed1','processContext':{'lpu':{'address':'1'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"
        self.move_incorrect_object = "{'processId':'example','transitionId':'c7c16b5c-75fa-4fc5-8912-cbf4af72fed1','processContext':{'lpu':{'address':1},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"
        self.move_incorrect_array = "{'processId':'example','transitionId':'c7c16b5c-75fa-4fc5-8912-cbf4af72fed1','processContext':{'lpu':{'address':'1'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]},'roleContext':{}}"

    @allure.feature("Тесты на дубликат параметров при создании заявки")
    def testCorrectValueInStringParameter(self):

        #переданы значения прописанных форматов в объекте и массиве
        success_create = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.success_create)
        Assertions.assert_json_value_by_name(success_create, 'success', True, 'Неожиданная ошибка при создании направления')
        processId = success_create.json()['processId']

        #передан неверный формат в объекте
        create_incorrect_value_in_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_incorrect_object)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_object, 'message', "Следующие поля имеют неправильный формат: Адрес МО\nDetails:\n[#/lpu/address] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передан неверный формат в массиве
        create_incorrect_value_in_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_incorrect_array)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_array, 'message', "Object reference not set to an instance of an object.",
                                             'Ошибка о неверном формате данных string не получена')

        #передачи неверных форматов в moveToStage
        self.move_incorrect_object = self.move_incorrect_object.replace('example', processId)
        self.move_incorrect_array = self.move_incorrect_array.replace('example', processId)

        move_incorrect_value_in_object = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_object)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_object, 'message', "Следующие поля имеют неправильный формат: Адрес МО\nDetails:\n[#/lpu/address] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        move_incorrect_value_in_array = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_array)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_array, 'message', "Object reference not set to an instance of an object.",
                                             'Ошибка о неверном формате данных string не получена')

        #передача корректных форматов
        self.success_move = self.success_move.replace('example', processId)
        success_move = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                         data=self.success_create)
        Assertions.assert_json_value_by_name(success_move, 'success', True,'Неожиданная ошибка при смене статуса направления')

@allure.epic("Проверки Plugins")
class TestProcessDuplicateValidator(BaseCase):

    def setup(self):

        self.to_stage2 = "a178f468-7c01-4e37-a07d-361a6864edf3"
        self.to_stage3 = "4c5912b5-89ee-44ef-bf9f-ee31b40068a3"

        self.create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_dublicate','InitialTransitionId':'b5ddca4f-bb06-439c-995d-358a64e89bd3','ProcessContext':{'lpu':{'address':'example'},'arrayLpu':[{'id':'1','idLpu':'test_array_value','isDeleted':false}]},'roleContext':{}}"
        self.another_create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_dublicate','InitialTransitionId':'b5ddca4f-bb06-439c-995d-358a64e89bd3','ProcessContext':{'lpu':{'address':'example'},'arrayLpu':[{'id':'1','idLpu':'test_array_value','isDeleted':false}]},'roleContext':{}}"
        self.no_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_dublicate','InitialTransitionId':'b5ddca4f-bb06-439c-995d-358a64e89bd3','ProcessContext':{'arrayLpu':[{'id':'1','idLpu':'test_array_value','isDeleted':false}]},'roleContext':{}}"
        self.no_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_dublicate','InitialTransitionId':'b5ddca4f-bb06-439c-995d-358a64e89bd3','ProcessContext':{'lpu':{'address':'example'}},'roleContext':{}}"

        self.move = "{'processId':'example','transitionId':'to_stage','processContext':{},'roleContext':{}}"

        self.create_again = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_dublicate','InitialTransitionId':'b5ddca4f-bb06-439c-995d-358a64e89bd3','ProcessContext':{'lpu':{'address':'example'},'arrayLpu':[{'id':'1','idLpu':'test_array_value','isDeleted':false}]},'roleContext':{}}"

        self.change_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/Validators/ProcessDuplicateValidator","name":"Проверка на дубликат заявки","messageOnError":"Найден дубликат заявки","description":"","type":"External","areaId":"bfe35b34-2824-4af6-95c9-49965998f081","schemaId":null,"parameter":"{\\"paths\\": [\\"arrayLpu[0].idLpu\\", \\"lpu.address\\"], \\"stages\\": [\\"fd29aadd-2f26-4d5a-90a3-e3dab1adedd9\\",\\"a22cfdd7-6a54-4ed2-9b49-6d527afae3d1\\"], \\"workFlow\\": \\"09872eef-6180-4f5f-9137-c33ce60ad416\\"}"}'.encode('UTF-8')
        self.comeback_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/Validators/ProcessDuplicateValidator","name":"Проверка на дубликат заявки","messageOnError":"Найден дубликат заявки","description":"","type":"External","areaId":"bfe35b34-2824-4af6-95c9-49965998f081","schemaId":null,"parameter":"{\\"paths\\": [\\"arrayLpu[0].idLpu\\", \\"lpu.address\\"], \\"stages\\": [\\"fd29aadd-2f26-4d5a-90a3-e3dab1adedd9\\"], \\"workFlow\\": \\"09872eef-6180-4f5f-9137-c33ce60ad416\\"}"}'.encode('UTF-8')

    @allure.feature("Тесты на дубликат параметров при создании заявки")
    def testDublicateProcess(self):

        #создать первоначальную заявку с проверкой на дубль двух параметров
        create = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},data=self.create)
        processId = create.json()['processId']
        humanFriendlyId = create.json()['humanFriendlyId']

        #попытка создать новую заявку
        create_for_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},data=self.create)
        Assertions.assert_json_value_by_name(create_for_error, 'message', f'По данной заявке найден дубль {humanFriendlyId}', 'Ошибка о дубле не получена')

        #изменить один из параметров и увидеть, что проверка на дубль идет только при полном совпадении всех параметров
        self.another_create = self.another_create.replace('example', f'{datetime.datetime.now()}')
        create_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},data=self.another_create)
        Assertions.assert_json_value_by_name(create_2, 'success', True, 'Неожиданная ошибка при создании направления')

        #не передано значение из объекта в проверке
        no_value_in_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},data=self.no_object)
        Assertions.assert_json_value_by_name(no_value_in_object, 'message', 'По данному jsonPath = lpu.address значение не найдено.', 'Неожиданная ошибка при создании направления без значения в объекте')

        #не передано значение из массива в проверке
        no_value_in_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.no_array)
        Assertions.assert_json_value_by_name(no_value_in_array, 'message','По данному jsonPath = arrayLpu[0].idLpu значение не найдено.','Неожиданная ошибка при создании направления без значения в массиве')

        #не передать в MoveToStage по отдельности значения из объекта и массива - проблем нет, т.к. в ProcessContext направления данные параметры уже есть

        #привести заявку к статусу 2
        replace_values = {'example': processId, 'to_stage': self.to_stage2}
        self.move = self.multiple_replace(self.move, replace_values)

        move_to_status2 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_to_status2, 'success', True, 'Неожиданная ошибка при смене статуса')

        #проверка что снова будет ошибка дубля при создании новой
        create_for_error_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.create)
        Assertions.assert_json_value_by_name(create_for_error_2, 'message',f'По данной заявке найден дубль {humanFriendlyId}','Ошибка о дубле не получена')

        #перевод в 3 статус
        self.move = self.move.replace(self.to_stage2, self.to_stage3)
        move_to_status3 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_to_status3, 'success', True, 'Неожиданная ошибка при смене статуса')

        #создание с теми же данными нового направления, чтобы проверить что ошибки не будет
        create_again = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                data=self.create_again)
        Assertions.assert_json_value_by_name(create_again, 'success', True, 'Неожиданная ошибка при создании направления')
        processId2 = create_again.json()['processId']

        #приводим созданное направление также в 3 статус дабы очистить стенд
        replace_values = {processId: processId2, self.to_stage3: self.to_stage2}
        self.move = self.multiple_replace(self.move, replace_values)

        move_to_status2_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_to_status2_2, 'success', True, 'Неожиданная ошибка при смене статуса')

        self.move = self.move.replace(self.to_stage2, self.to_stage3)
        move_to_status3_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_to_status3_2, 'success', True, 'Неожиданная ошибка при смене статуса')

        #добавить к внешнему валидатору еще один конечный stage (status2) и создать новое направление
        update_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/9826b1fa-2866-4243-9c92-7d36431877ba', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.change_validator)
        Assertions.assert_json_value_by_name(update_validator, 'success', True, 'Обновление валидатора прошло неуспешно')

        create_again_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                data=self.create_again)
        Assertions.assert_json_value_by_name(create_again_2, 'success', True, 'Неожиданная ошибка при создании направления')
        processId3 = create_again_2.json()['processId']
        humanFriendlyId2 = create_again_2.json()['humanFriendlyId']

        #проверка что новое создать нельзя
        create_for_error_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                         data=self.create_again)
        Assertions.assert_json_value_by_name(create_for_error_3, 'message',f'По данной заявке найден дубль {humanFriendlyId2}','Ошибка о дубле не получена')

        #проверить что при переводе во второй статус можно будет создать новое направление
        replace_values = {processId2: processId3, self.to_stage3: self.to_stage2}
        self.move = self.multiple_replace(self.move, replace_values)
        move_old_to_status2 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_old_to_status2, 'success', True, 'Неожиданная ошибка при смене статуса')

        create_new = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},data=self.create_again)
        Assertions.assert_json_value_by_name(create_new, 'success', True, 'Неожиданная ошибка при создании направления')
        processIdLast = create_new.json()['processId']

        #проверить, что старое сдвинется в 3 статус
        self.move = self.move.replace(self.to_stage2, self.to_stage3)
        move_old_to_status3 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_old_to_status3, 'success', True, 'Неожиданная ошибка при смене статуса')

        #довести новое направление до 3 статуса для очистки данных
        replace_values = {processId3: processIdLast, self.to_stage3: self.to_stage2}
        self.move = self.multiple_replace(self.move, replace_values)

        move_new_to_status2 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_new_to_status2, 'success', True,'Неожиданная ошибка при смене статуса')

        self.move = self.move.replace(self.to_stage2, self.to_stage3)
        move_new_to_status3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.move)
        Assertions.assert_json_value_by_name(move_new_to_status3, 'success', True,'Неожиданная ошибка при смене статуса')

        #убрать у валидатора лишний конечный статус
        comeback_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/9826b1fa-2866-4243-9c92-7d36431877ba',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.comeback_validator)
        Assertions.assert_json_value_by_name(comeback_validator, 'success', True,'Обновление валидатора прошло неуспешно')

@allure.epic("Проверки Plugins")
class TestDateValidatorValidate(BaseCase):

    def setup(self):

        self.create_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'f80d63f6-8dc2-4c8b-b769-a7ff93aa66ae','ProcessContext':{'lpu':{'date':'test_value'}},'roleContext':{}}"
        self.move_object = "{'processId':'example','transitionId':'41163af8-0e76-4071-a2e0-8a4fedb9e203','processContext':{'lpu':{'date':'test_value'}},'roleContext':{}}"

        self.change_validator_to_array = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/Validate?argument=arrayLpu.items.arrayDate","MessageOnError":"Формат даты некорректный"}'.encode('UTF-8')
        self.change_validator_back = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/Validate?argument=lpu.date","MessageOnError":"Формат даты некорректный"}'.encode('UTF-8')

        self.create_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'f80d63f6-8dc2-4c8b-b769-a7ff93aa66ae','ProcessContext':{'arrayLpu':[{'id':'1','arrayDate':'test_array_value','isDeleted':false}]},'roleContext':{}}"
        self.move_array = "{'processId':'example','transitionId':'41163af8-0e76-4071-a2e0-8a4fedb9e203','processContext':{'arrayLpu':[{'id':'1','arrayDate':'test_array_value','isDeleted':false}]},'roleContext':{}}"

    @allure.feature("Тесты на проверку формата даты в объекте")
    def testValidateDateObject(self):

        #запрос с неверным форматом даты (текст)
        create_object_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_text, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #неверный формат числа
        self.create_object = self.create_object.replace('test_value', '2021-13-28')
        create_object_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_date, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #неверный формат времени
        self.create_object = self.create_object.replace('2021-13-28', '2021-12-30T11:61:00Z')
        create_object_time = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_time, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #передать три формата даты и получить успех
        self.create_object = self.create_object.replace('2021-12-30T11:61:00Z', '2021-12-28')
        create_object_1 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_1, 'success', True, 'Создание направления завершилось неуспешно')
        processId_object_1 = create_object_1.json()['processId']

        self.create_object = self.create_object.replace('2021-12-28', '2021-12-30T11:00:00Z')
        create_object_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_2, 'success', True, 'Создание направления завершилось неуспешно')
        processId_object_2 = create_object_2.json()['processId']

        self.create_object = self.create_object.replace('2021-12-30T11:00:00Z', '2021-12-28T10:00:00+03:00')
        create_object_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_3, 'success', True, 'Создание направления завершилось неуспешно')
        processId_object_3 = create_object_3.json()['processId']

        #прописываем для MoveToStage первый processId и пробуем повторно передать не те форматы
        self.move_object = self.move_object.replace('example', processId_object_1)
        move_object_text = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_text, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        self.move_object = self.move_object.replace('test_value', '2021-13-28')
        move_object_date = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_date, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        self.move_object = self.move_object.replace('2021-13-28', '2021-12-30T11:61:00Z')
        move_object_time = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_time, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #три ранее успешно созданных направления двигаем передавая в таком же форматы даты
        self.move_object = self.move_object.replace('2021-12-30T11:61:00Z', '2021-12-28')
        move_object_1 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_1, 'success', True, 'Смена статуса направления завершилась неуспешно')

        replace_values = {'2021-12-28': '2021-12-30T11:00:00Z', processId_object_1: processId_object_2}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_object_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_2, 'success', True, 'Смена статуса направления завершилась неуспешно')

        replace_values = {'2021-12-30T11:00:00Z': '2021-12-28T10:00:00+03:00', processId_object_2: processId_object_3}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_object_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_3, 'success', True,'Смена статуса направления завершилась неуспешно')

    @allure.feature("Тесты на проверку формата даты в массиве")
    def testValidateDateArray(self):

        #поменять валидатор на проверку значения массива
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/d3d7ce9e-3541-4738-9382-dd8f753d2e85',
                                           headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.change_validator_to_array)
        Assertions.assert_json_value_by_name(change_validator, 'success', True, 'Смена валидатора прошла неуспешно')

        #запрос с неверным форматом даты (текст)
        create_array_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_text, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #неверный формат числа
        self.create_array = self.create_array.replace('test_array_value', '2021-12-32')
        create_array_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_date, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #неверный формат времени
        self.create_array = self.create_array.replace('2021-12-32', '2021-12-28T10:70:00+03:00')
        create_array_time = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_time, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #передать три формата даты и получить успех
        self.create_array = self.create_array.replace('2021-12-28T10:70:00+03:00', '2021-12-28')
        create_array_1 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_1, 'success', True, 'Создание направления прошло неуспешно')
        processId_array_1 = create_array_1.json()['processId']

        self.create_array = self.create_array.replace('2021-12-28', '2021-12-30T11:00:00Z')
        create_array_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_2, 'success', True, 'Создание направления прошло неуспешно')
        processId_array_2 = create_array_2.json()['processId']

        self.create_array = self.create_array.replace('2021-12-30T11:00:00Z', '2021-12-28T10:00:00+03:00')
        create_array_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_3, 'success', True, 'Создание направления прошло неуспешно')
        processId_array_3 = create_array_3.json()['processId']

        #прописываем для MoveToStage первый processId и пробуем повторно передать не те форматы
        self.move_array = self.move_array.replace('example', processId_array_1)
        move_array_text = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_text, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        self.move_array = self.move_array.replace('test_array_value', '2021-12-32')
        move_array_date = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_date, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        self.move_array = self.move_array.replace('2021-12-32', '2021-12-28T10:70:00+03:00')
        move_array_time = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_time, 'message', 'Формат даты некорректный', 'Ошибка о некорректной дате не получена')

        #три ранее успешно созданных направления двигаем передавая в таком же форматы даты
        self.move_array = self.move_array.replace('2021-12-28T10:70:00+03:00', '2021-12-28')
        move_array_1 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_1, 'success', True, 'Смена статуса направления прошла неуспешно')

        replace_values = {'2021-12-28': '2021-12-30T11:00:00Z', processId_array_1: processId_array_2}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_array_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                       data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_2, 'success', True,'Смена статуса направления прошла неуспешно')

        replace_values = {'2021-12-30T11:00:00Z': '2021-12-28T10:00:00+03:00', processId_array_2: processId_array_3}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_array_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                       data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_3, 'success', True,'Смена статуса направления прошла неуспешно')

        #поменять валидатор обратно
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/d3d7ce9e-3541-4738-9382-dd8f753d2e85',
                                           headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'}, data=self.change_validator_back)
        Assertions.assert_json_value_by_name(change_validator_back, 'success', True, 'Смена валидатора прошла неуспешно')

@allure.epic("Проверки Plugins")
class TestDateValidatorAfterToday(BaseCase):
    def setup(self):

        self.create_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'73db4083-0581-4ee4-b541-1a600a187aba','ProcessContext':{'lpu':{'afterDate':'test_value'}},'roleContext':{}}"
        self.move_object = "{'processId':'example','transitionId':'79526abf-f79a-4298-a5a2-ab3dcf417328','processContext':{'lpu':{'afterDate':'test_value'}},'roleContext':{}}"

        self.change_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/AfterToday?argument=lpu.afterDate&time=false","messageOnError":"Ошибка при проверке даты, которая должна быть больше текущей"}'.encode('UTF-8')
        self.change_validator_back = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/AfterToday?argument=lpu.afterDate&time=true","messageOnError":"Ошибка при проверке даты, которая должна быть больше текущей"}'.encode('UTF-8')

        self.validator_to_array = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/AfterToday?argument=arrayLpu.items.arrayAfterDate&time=true","messageOnError":"Ошибка при проверке даты, которая должна быть больше текущей"}'.encode('UTF-8')
        self.change_array_to_false = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/AfterToday?argument=arrayLpu.items.arrayAfterDate&time=false","messageOnError":"Ошибка при проверке даты, которая должна быть больше текущей"}'.encode('UTF-8')

        self.create_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'73db4083-0581-4ee4-b541-1a600a187aba','ProcessContext':{'arrayLpu':[{'id':'1','arrayAfterDate':'test_value','isDeleted':false}]},'roleContext':{}}"
        self.move_array = "{'processId':'example','transitionId':'79526abf-f79a-4298-a5a2-ab3dcf417328','processContext':{'arrayLpu':[{'id':'1','arrayAfterDate':'test_value','isDeleted':false}]},'roleContext':{}}"

    @allure.feature("Тесты в объекте на то, что проверяемая дата больше текущей")
    def testAfterTodayObject(self):

        #передать текст
        create_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_text, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #передать сегодняшний день 2022-08-12 и получить ошибку
        self.create_object = self.create_object.replace('test_value', f'{datetime.date.today()}')
        create_today_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_date, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #передать завтрашний день и всё ок
        self.create_object = self.create_object.replace(f'{datetime.date.today()}', f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_tomorrow_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_tomorrow_date, 'success', True, 'Создание направления закончилось ошибкой')
        processId = create_tomorrow_date.json()['processId']

        #передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}', f'{datetime.date.today()}' + 'T00:00:00Z')
        create_today_time_00 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_00, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today()}' + 'T20:00:00Z')
        create_today_time_20 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_20, 'success', True, 'Создание направления закончилось ошибкой')
        processId_1 = create_today_time_20.json()['processId']

        #повторить манипуляции с 2022-08-12T10:00:00+03:00
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T20:00:00Z', f'{datetime.date.today()}' + 'T03:00:00+03:00')
        create_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_00_3, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00', f'{datetime.date.today()}' + 'T20:00:00+03:00')
        create_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_20_3, 'success', True, 'Создание направления закончилось ошибкой')
        processId_2 = create_today_time_20_3.json()['processId']

        #в запрос moveToStage повторить манипуляции
        self.move_object = self.move_object.replace('example', processId)
        move_object_text = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_text, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        # передать сегодняшний день и получить ошибку
        self.move_object = self.move_object.replace('test_value', f'{datetime.date.today()}')
        move_today_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_date, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # передать завтрашний день и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today()}', f'{datetime.date.today() + datetime.timedelta(days=1)}')
        move_tomorrow_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_tomorrow_date, 'success', True,'Смена статуса направления закончилась ошибкой')

        # передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и получить ошибку
        replace_values = {processId: processId_1, f'{datetime.date.today() + datetime.timedelta(days=1)}': f'{datetime.date.today()}' + 'T00:00:00Z'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_today_time_00 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_00, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today()}' + 'T20:00:00Z')
        move_today_time_20 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_20, 'success', True,'Смена статуса направления закончилась ошибкой')

        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        replace_values = {processId_1: processId_2, f'{datetime.date.today()}' + 'T20:00:00Z': f'{datetime.date.today()}' + 'T03:00:00+03:00'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_00_3, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00',f'{datetime.date.today()}' + 'T20:00:00+03:00')
        move_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_20_3, 'success', True,'Смена статуса направления закончилась ошибкой')

        #изменить в валидаторе на time=false
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/59074486-6131-49d0-ab40-660488ed0528', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.change_validator)
        Assertions.assert_json_value_by_name(change_validator,'success', True, 'Изменение валидатора прошло неуспешно')

        #передать данные в формате с часами раньше текущего за сегодняшний день и не получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00', f'{datetime.date.today()}' + 'T00:00:00Z')
        create_new = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_object)
        Assertions.assert_json_value_by_name(create_new, 'success', True, 'Создание направления завершилось неуспешно')
        processId_new = create_new.json()['processId']

        #передать вчерашний день и получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today() + datetime.timedelta(days=-1)}')
        create_new_yesterday = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                     data=self.create_object)
        Assertions.assert_json_value_by_name(create_new_yesterday, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        #повторить манипуляции с moveToStage
        replace_values = {processId_2: processId_new,f'{datetime.date.today()}' + 'T20:00:00+03:00': f'{datetime.date.today() + datetime.timedelta(days=-1)}'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_new_yesterday = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_object)
        Assertions.assert_json_value_by_name(move_new_yesterday, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        self.move_object = self.move_object.replace(f'{datetime.date.today() + datetime.timedelta(days=-1)}', f'{datetime.date.today()}' + 'T00:00:00Z')
        move_new = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_object)
        Assertions.assert_json_value_by_name(move_new, 'success', True, 'Создание направления завершилось неуспешно')

        #возвращаем значение валидатора
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/59074486-6131-49d0-ab40-660488ed0528', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.change_validator_back)
        Assertions.assert_json_value_by_name(change_validator_back,'success', True, 'Изменение валидатора прошло неуспешно')

    @allure.feature("Тесты в массиве на то, что проверяемая дата больше текущей")
    def testAfterTodayArray(self):

        #сменить параметр для проверки
        new_parameter_in_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/59074486-6131-49d0-ab40-660488ed0528', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.validator_to_array)
        Assertions.assert_json_value_by_name(new_parameter_in_validator,'success', True, 'Изменение валидатора прошло неуспешно')

        #передать текст
        create_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                              data=self.create_array)
        Assertions.assert_json_value_by_name(create_text, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #передать сегодняшний день 2022-08-12 и получить ошибку
        self.create_array = self.create_array.replace('test_value', f'{datetime.date.today()}')
        create_today_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_date, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #передать завтрашний день и всё ок
        self.create_array = self.create_array.replace(f'{datetime.date.today()}', f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_tomorrow_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_tomorrow_date, 'success', True, 'Создание направления закончилось ошибкой')
        processId = create_tomorrow_date.json()['processId']

        #передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и получить ошибку
        self.create_array = self.create_array.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}', f'{datetime.date.today()}' + 'T00:00:00Z')
        create_today_time_00 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_00, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        #докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today()}' + 'T20:00:00Z')
        create_today_time_20 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_20, 'success', True, 'Создание направления закончилось ошибкой')
        processId_1 = create_today_time_20.json()['processId']

        #повторить манипуляции с 2022-08-12T10:00:00+03:00
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T20:00:00Z', f'{datetime.date.today()}' + 'T03:00:00+03:00')
        create_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_00_3, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00', f'{datetime.date.today()}' + 'T20:00:00+03:00')
        create_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_20_3, 'success', True, 'Создание направления закончилось ошибкой')
        processId_2 = create_today_time_20_3.json()['processId']

        #в запрос moveToStage повторить манипуляции
        self.move_array = self.move_array.replace('example', processId)
        move_array_text = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_text, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей', 'Ошибка о некорректной дате не получена')

        # передать сегодняшний день и получить ошибку
        self.move_array = self.move_array.replace('test_value', f'{datetime.date.today()}')
        move_today_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_date, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # передать завтрашний день и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today()}', f'{datetime.date.today() + datetime.timedelta(days=1)}')
        move_tomorrow_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_tomorrow_date, 'success', True,'Смена статуса направления закончилась ошибкой')

        # передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и получить ошибку
        replace_values = {processId: processId_1, f'{datetime.date.today() + datetime.timedelta(days=1)}': f'{datetime.date.today()}' + 'T00:00:00Z'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_today_time_00 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_00, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today()}' + 'T20:00:00Z')
        move_today_time_20 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_20, 'success', True,'Смена статуса направления закончилась ошибкой')

        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        replace_values = {processId_1: processId_2, f'{datetime.date.today()}' + 'T20:00:00Z': f'{datetime.date.today()}' + 'T03:00:00+03:00'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_00_3, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00',f'{datetime.date.today()}' + 'T20:00:00+03:00')
        move_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_20_3, 'success', True,'Смена статуса направления закончилась ошибкой')

        #изменить в валидаторе на time=false
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/59074486-6131-49d0-ab40-660488ed0528', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.change_array_to_false)
        Assertions.assert_json_value_by_name(change_validator,'success', True, 'Изменение валидатора прошло неуспешно')

        #передать данные в формате с часами раньше текущего за сегодняшний день и не получить ошибку
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00', f'{datetime.date.today()}' + 'T00:00:00Z')
        create_new = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                             data=self.create_array)
        Assertions.assert_json_value_by_name(create_new, 'success', True, 'Создание направления завершилось неуспешно')
        processId_new = create_new.json()['processId']

        #передать вчерашний день и получить ошибку
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T00:00:00Z', f'{datetime.date.today() + datetime.timedelta(days=-1)}')
        create_new_yesterday = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                     data=self.create_array)
        Assertions.assert_json_value_by_name(create_new_yesterday, 'message','Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        #повторить манипуляции с moveToStage
        replace_values = {processId_2: processId_new,f'{datetime.date.today()}' + 'T20:00:00+03:00': f'{datetime.date.today() + datetime.timedelta(days=-1)}'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_new_yesterday = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_array)
        Assertions.assert_json_value_by_name(move_new_yesterday, 'message', 'Ошибка при проверке даты, которая должна быть больше текущей','Ошибка о некорректной дате не получена')

        self.move_array = self.move_array.replace(f'{datetime.date.today() + datetime.timedelta(days=-1)}', f'{datetime.date.today()}' + 'T00:00:00Z')
        move_new = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_array)
        Assertions.assert_json_value_by_name(move_new, 'success', True, 'Создание направления завершилось неуспешно')

        #возвращаем значение валидатора
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/59074486-6131-49d0-ab40-660488ed0528', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.change_validator_back)
        Assertions.assert_json_value_by_name(change_validator_back,'success', True, 'Изменение валидатора прошло неуспешно')

#@allure.epic("Проверки Plugins")
#class TestDateValidatorBeforeToday(BaseCase):

#@allure.epic("Проверки Plugins")
#class TestDateValidatorCompareDates(BaseCase):


#проверка ValidatePhone
