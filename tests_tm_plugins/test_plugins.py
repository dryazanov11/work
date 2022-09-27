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
        self.snp_no_value_in_array = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check_required","InitialTransitionId":"917c2fea-3173-48e3-ac8c-bb3a24ff7c1f","ProcessContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"},"arrayLpu":[{"id":"1","isDeleted":false},{"id":"2","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'

        self.mts_no_values_from_object = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{},"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.mts_no_object = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"arrayLpu":[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'
        self.mts_no_array = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{"idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","address":"1"}},"roleContext":{}}'
        self.mts_no_value_in_array = '{"processId":"example","transitionId":"84e1529e-33d6-4580-acec-373b0e430290","processContext":{"lpu":{"address":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682"},"arrayLpu":[{"id":"1","isDeleted":false},{"id":"2","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]},"roleContext":{}}'

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

        #не передать при создании значение из первого элемента массива
        snp_no_value_in_array_1 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.snp_no_value_in_array)
        Assertions.assert_json_value_by_name(snp_no_value_in_array_1, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО\nDetails:\n[#/arrayLpu/0/idLpu] - Поле не заполнено или отсутствует',
                                             'Получена неожиданная ошибка')

        #не передать при создании значение из второго элемента массива
        self.snp_no_value_in_array = self.snp_no_value_in_array.replace('[{"id":"1","isDeleted":false},{"id":"2","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]', '[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]')
        snp_no_value_in_array_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.snp_no_value_in_array)
        Assertions.assert_json_value_by_name(snp_no_value_in_array_2, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО\nDetails:\n[#/arrayLpu/1/idLpu] - Поле не заполнено или отсутствует',
                                             'Получена неожиданная ошибка')

        #не передать при создании значение из обоих элементов массива
        self.snp_no_value_in_array = self.snp_no_value_in_array.replace('[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]', '[{"id":"1","isDeleted":false},{"id":"2","isDeleted":false}]')
        snp_no_value_in_array_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.snp_no_value_in_array)
        Assertions.assert_json_value_by_name(snp_no_value_in_array_3, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО, Идентификатор МО\nDetails:\n[#/arrayLpu/0/idLpu] - Поле не заполнено или отсутствует\n[#/arrayLpu/1/idLpu] - Поле не заполнено или отсутствует',
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

        #не передать значение из 1 элемента массива в moveToStage
        self.mts_no_value_in_array = self.mts_no_value_in_array.replace('example', processId)
        mts_no_value_in_array_1 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_value_in_array)
        Assertions.assert_json_value_by_name(mts_no_value_in_array_1, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО\nDetails:\n[#/arrayLpu/0/idLpu] - Поле не заполнено или отсутствует',
                                             'Получена неожиданная ошибка')

        #не передать значение из 2 элемента массива в movetostage
        self.mts_no_value_in_array = self.mts_no_value_in_array.replace('[{"id":"1","isDeleted":false},{"id":"2","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false}]', '[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]')
        mts_no_value_in_array_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_value_in_array)
        Assertions.assert_json_value_by_name(mts_no_value_in_array_2, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО\nDetails:\n[#/arrayLpu/1/idLpu] - Поле не заполнено или отсутствует',
                                             'Получена неожиданная ошибка')

        #не передать оба значение из двух элементов массива
        self.mts_no_value_in_array = self.mts_no_value_in_array.replace('[{"id":"1","idLpu":"3b4b37cd-ef0f-4017-9eb4-2fe49142f682","isDeleted":false},{"id":"2","isDeleted":false}]', '[{"id":"1","isDeleted":false},{"id":"2","isDeleted":false}]')
        mts_no_value_in_array_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                    data=self.mts_no_value_in_array)
        Assertions.assert_json_value_by_name(mts_no_value_in_array_3, 'message','Следующие поля отсутствуют или не заполнены: Идентификатор МО, Идентификатор МО\nDetails:\n[#/arrayLpu/0/idLpu] - Поле не заполнено или отсутствует\n[#/arrayLpu/1/idLpu] - Поле не заполнено или отсутствует',
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

        self.success_create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'lpu':{'address':'test_value_object'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'test_value_array','isDeleted':false}]},'roleContext':{}}"
        self.create_incorrect_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'lpu':{'address':1},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'test_value_array','isDeleted':false}]},'roleContext':{}}"
        self.create_incorrect_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'lpu':{'address':'test_value_object'},'arrayLpu':[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"

        self.success_move = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'lpu':{'address':'1'},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"
        self.move_incorrect_object = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'lpu':{'address':1},'arrayLpu':[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"
        self.move_incorrect_array = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'lpu':{'address':'1'},'arrayLpu':[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]},'roleContext':{}}"

        self.create_allow = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_allowable_value','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'lpu':{'allowableValue':'test_value_object'},'arrayLpu':[{'id':'1','allowableValueArray':'888','isDeleted':false},{'id':'2','allowableValueArray':'test_value_array','isDeleted':false}]},'roleContext':{}}"
        self.move_allow = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'lpu':{'allowableValue':'777'},'arrayLpu':[{'id':'1','allowableValueArray':'888','isDeleted':false},{'id':'2','allowableValueArray':'test_value_array','isDeleted':false}]},'roleContext':{}}"

    @allure.feature("Тесты на соответствие переданного формата тому, что указан у параметра string")
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

        #передан неверный формат в 1 элементе массива
        create_incorrect_value_in_array_1 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_incorrect_array)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_array_1, 'message', "Следующие поля имеют неправильный формат: Дата\nDetails:\n[#/arrayLpu/0/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передан неверный формат в 2 элементе массива
        self.create_incorrect_array = self.create_incorrect_array.replace("[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]", "[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]")
        create_incorrect_value_in_array_2 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_incorrect_array)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_array_2, 'message', "Следующие поля имеют неправильный формат: Дата\nDetails:\n[#/arrayLpu/1/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передан неверный формат в обоих элементах массива
        self.create_incorrect_array = self.create_incorrect_array.replace("[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]", "[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]")
        create_incorrect_value_in_array_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_incorrect_array)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_array_3, 'message', "Следующие поля имеют неправильный формат: Дата, Дата\nDetails:\n[#/arrayLpu/0/arrayDate] - Неверный формат поля\n[#/arrayLpu/1/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передачи неверных форматов в moveToStage
        self.move_incorrect_object = self.move_incorrect_object.replace('example', processId)
        self.move_incorrect_array = self.move_incorrect_array.replace('example', processId)

        move_incorrect_value_in_object = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_object)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_object, 'message', "Следующие поля имеют неправильный формат: Адрес МО\nDetails:\n[#/lpu/address] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передан неверный формат в 1 элементе массива
        move_incorrect_value_in_array_1 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_array)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_array_1, 'message', "Следующие поля имеют неправильный формат: Дата\nDetails:\n[#/arrayLpu/0/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #во 2 элементе
        self.move_incorrect_array = self.move_incorrect_array.replace("[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':'2022-08-15','isDeleted':false}]", "[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]")
        move_incorrect_value_in_array_2 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_array)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_array_2, 'message', "Следующие поля имеют неправильный формат: Дата\nDetails:\n[#/arrayLpu/1/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #в обоих элементах массива неверный формат
        self.move_incorrect_array = self.move_incorrect_array.replace("[{'id':'1','arrayDate':'2022-08-15','isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]", "[{'id':'1','arrayDate':1,'isDeleted':false},{'id':'2','arrayDate':1,'isDeleted':false}]")
        move_incorrect_value_in_array_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_incorrect_array)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_array_3, 'message', "Следующие поля имеют неправильный формат: Дата, Дата\nDetails:\n[#/arrayLpu/0/arrayDate] - Неверный формат поля\n[#/arrayLpu/1/arrayDate] - Неверный формат поля",
                                             'Ошибка о неверном формате данных string не получена')

        #передача корректных форматов
        self.success_move = self.success_move.replace('example', processId)
        success_move = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                         data=self.success_create)
        Assertions.assert_json_value_by_name(success_move, 'success', True,'Неожиданная ошибка при смене статуса направления')

    @allure.feature("Тесты на соответствие переданного значения тому, что указан у параметра string как допустимое")
    def testAllowableValueInStringParameter(self):

        #передать корректно значения
        create_correct = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_allow)
        Assertions.assert_json_value_by_name(create_correct, 'success', True, 'Неожиданная ошибка при создании направления')
        processId = create_correct.json()['processId']

        #передать в объекте недопустимое значение
        self.create_allow = self.create_allow.replace('test_value_object', 'incorrect_value')
        create_incorrect_value_in_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_allow)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_object, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение\nDetails:\n[#/lpu/allowableValue] - Значение \"incorrect_value\" не соответствует требуемому.",
                                             'Ошибка при создании направления отличается от ожидаемой')

        #передать недопустимое значение в объекте и первом элементе массива
        self.create_allow = self.create_allow.replace('888', '999')
        create_incorrect_value_both = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_allow)
        Assertions.assert_json_value_by_name(create_incorrect_value_both, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение, Допустимое значение\nDetails:\n[#/lpu/allowableValue] - Значение \"incorrect_value\" не соответствует требуемому.\n[#/arrayLpu/0/allowableValueArray] - Значение \"999\" не соответствует требуемому.",
                                             'Ошибка при создании направления отличается от ожидаемой')

        #передать во втором элементе массива недопустимое значение
        replace_values = {'incorrect_value': 'test_value_object', '999': '888', 'test_value_array': 'incorrect_value'}
        self.create_allow = self.multiple_replace(self.create_allow, replace_values)
        create_incorrect_value_in_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.create_allow)
        Assertions.assert_json_value_by_name(create_incorrect_value_in_array, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение\nDetails:\n[#/arrayLpu/1/allowableValueArray] - Значение \"incorrect_value\" не соответствует требуемому.",
                                             'Ошибка при создании направления отличается от ожидаемой')

        #смена статуса и в объекте недопустимое значение
        self.move_allow = self.move_allow.replace('example', processId)
        move_incorrect_value_in_object = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_allow)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_object, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение\nDetails:\n[#/lpu/allowableValue] - Значение \"777\" не соответствует требуемому.",
                                             'Ошибка при смене статуса направления отличается от ожидаемой')

        #смена статуса и недопустимое значение в объекте и первом элементе массива
        self.move_allow = self.move_allow.replace('888', '1000')
        move_incorrect_value_both = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_allow)
        Assertions.assert_json_value_by_name(move_incorrect_value_both, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение, Допустимое значение\nDetails:\n[#/lpu/allowableValue] - Значение \"777\" не соответствует требуемому.\n[#/arrayLpu/0/allowableValueArray] - Значение \"1000\" не соответствует требуемому.",
                                             'Ошибка при смене статуса направления отличается от ожидаемой')

        #смена статуса и во втором элементе массива недопустимое значение
        replace_values = {'1000': '888', '777': '999', 'test_value_array': 'incorrect_value'}
        self.move_allow = self.multiple_replace(self.move_allow, replace_values)
        move_incorrect_value_in_array = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_allow)
        Assertions.assert_json_value_by_name(move_incorrect_value_in_array, 'message', "Следующие поля имеют неверно заполненные данные: Допустимое значение\nDetails:\n[#/arrayLpu/1/allowableValueArray] - Значение \"incorrect_value\" не соответствует требуемому.",
                                             'Ошибка при смене статуса направления отличается от ожидаемой')

        #смена статуса передав всё верно
        self.move_allow = self.move_allow.replace('incorrect_value', 'test_value_array')
        move_correct = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                         data=self.move_allow)
        Assertions.assert_json_value_by_name(move_correct, 'success', True, 'Смена статуса направления завершилась неуспешно')

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

@allure.epic("Проверки Plugins")
class TestDateValidatorBeforeToday(BaseCase):
    def setup(self):
        self.create_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'e9ba3105-83f5-480b-a61e-4abb7bc95685','ProcessContext':{'lpu':{'beforeDate':'test_value'}},'roleContext':{}}"
        self.move_object = "{'processId':'example','transitionId':'ed8a23d8-3efd-4ffe-bdcd-920ffaf3a5e8','processContext':{'lpu':{'beforeDate':'test_value'}},'roleContext':{}}"

        self.change_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/BeforeToday?argument=lpu.beforeDate&time=false","messageOnError":"Ошибка при проверке даты, которая должна быть меньше текущей"}'.encode('UTF-8')
        self.change_validator_back = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/BeforeToday?argument=lpu.beforeDate&time=true","messageOnError":"Ошибка при проверке даты, которая должна быть меньше текущей"}'.encode('UTF-8')

        self.validator_to_array = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/BeforeToday?argument=arrayLpu.items.arrayBeforeDate&time=true","messageOnError":"Ошибка при проверке даты, которая должна быть меньше текущей"}'.encode('UTF-8')
        self.change_array_to_false = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/BeforeToday?argument=arrayLpu.items.arrayBeforeDate&time=false","messageOnError":"Ошибка при проверке даты, которая должна быть меньше текущей"}'.encode('UTF-8')

        self.create_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'e9ba3105-83f5-480b-a61e-4abb7bc95685','ProcessContext':{'arrayLpu':[{'id':'1','arrayBeforeDate':'test_value','isDeleted':false}]},'roleContext':{}}"
        self.move_array = "{'processId':'example','transitionId':'ed8a23d8-3efd-4ffe-bdcd-920ffaf3a5e8','processContext':{'arrayLpu':[{'id':'1','arrayBeforeDate':'test_value','isDeleted':false}]},'roleContext':{}}"

    @allure.feature("Тесты в объекте на то, что проверяемая дата больше текущей")
    def testBeforTodayObject(self):
        # передать текст
        create_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                      data=self.create_object)
        Assertions.assert_json_value_by_name(create_text, 'message','Ошибка при проверке даты, которая должна быть меньше текущей',
                                             'Ошибка о некорректной дате не получена')

        # передать сегодняшний день и всё ок
        self.create_object = self.create_object.replace('test_value', f'{datetime.date.today()}')
        create_today_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_date, 'success',True,'Создание направления закончилось ошибкой')
        processId = create_today_date.json()['processId']

        # передать завтрашний день и получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today()}',f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_tomorrow_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_object)
        Assertions.assert_json_value_by_name(create_tomorrow_date, 'message','Ошибка при проверке даты, которая должна быть меньше текущей',
                                             'Ошибка о некорректной дате не получена')

        # передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и не получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}',f'{datetime.date.today()}' + 'T00:00:00Z')
        create_today_time_00 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_00, 'success', True,'Создание направления закончилось ошибкой')
        processId_1 = create_today_time_00.json()['processId']

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T00:00:00Z',f'{datetime.date.today()}' + 'T20:00:00Z')
        create_today_time_20 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_20, 'message','Ошибка при проверке даты, которая должна быть меньше текущей',
                                             'Ошибка о некорректной дате не получена')

        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T20:00:00Z',f'{datetime.date.today()}' + 'T03:00:00+03:00')
        create_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_00_3, 'success', True,'Создание направления закончилось ошибкой')
        processId_2 = create_today_time_00_3.json()['processId']

        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00',f'{datetime.date.today()}' + 'T20:00:00+03:00')
        create_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create_object)
        Assertions.assert_json_value_by_name(create_today_time_20_3, 'message','Ошибка при проверке даты, которая должна быть меньше текущей',
                                             'Ошибка о некорректной дате не получена')

        # в запрос moveToStage повторить манипуляции
        self.move_object = self.move_object.replace('example', processId)
        move_object_text = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_text, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать завтрашний день и получить ошибку
        self.move_object = self.move_object.replace('test_value',f'{datetime.date.today() + datetime.timedelta(days=1)}')
        move_tomorrow_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_tomorrow_date, 'message','Ошибка при проверке даты, которая должна быть меньше текущей',
                                             'Ошибка о некорректной дате не получена')

        # передать сегодняшний день и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}', f'{datetime.date.today()}')
        move_today_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_date, 'success', True,'Смена статуса направления закончилась ошибкой')

        # докинуть данные в формате 2022-08-12T20:00:00Z сегодняшнего дня, чтобы время было больше текущего и получить ошибку
        replace_values = {processId: processId_1,f'{datetime.date.today()}': f'{datetime.date.today()}' + 'T20:00:00Z'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)
        move_today_time_20 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_20, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать данные в формате 2022-08-12T00:00:00Z с утренним временем сегодняшнего дня и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today()}' + 'T20:00:00Z', f'{datetime.date.today()}' + 'T00:00:00Z')
        move_today_time_00 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_00, 'success',True,'Ошибка о некорректной дате не получена')

        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        replace_values = {processId_1: processId_2,f'{datetime.date.today()}' + 'T00:00:00Z': f'{datetime.date.today()}' + 'T20:00:00+03:00'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_20_3, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # убрать в этом формате часы сегодняшнего дня, чтобы время было раньше текущего и всё ок
        self.move_object = self.move_object.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00',f'{datetime.date.today()}' + 'T03:00:00+03:00')
        move_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_object)
        Assertions.assert_json_value_by_name(move_today_time_00_3, 'success', True,'Смена статуса направления закончилась ошибкой')

        # изменить в валидаторе на time=false
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/b7795021-9e8b-400a-bd04-69de0dff72bc',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                           data=self.change_validator)
        Assertions.assert_json_value_by_name(change_validator, 'success', True, 'Изменение валидатора прошло неуспешно')

        # передать данные в формате с часами позже текущего за сегодняшний день и не получить ошибку
        create_new = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                     data=self.create_object)
        Assertions.assert_json_value_by_name(create_new, 'success', True, 'Создание направления завершилось неуспешно')
        processId_new = create_new.json()['processId']

        # передать завтрашний день и получить ошибку
        self.create_object = self.create_object.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00',f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_new_tomorrow = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_object)
        Assertions.assert_json_value_by_name(create_new_tomorrow, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # повторить манипуляции с moveToStage
        replace_values = {processId_2: processId_new,f'{datetime.date.today()}' + 'T03:00:00+03:00': f'{datetime.date.today() + datetime.timedelta(days=1)}'}
        self.move_object = self.multiple_replace(self.move_object, replace_values)

        move_new_tomorrow = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_object)
        Assertions.assert_json_value_by_name(move_new_tomorrow, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        self.move_object = self.move_object.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}',f'{datetime.date.today()}' + 'T20:00:00Z')
        move_new = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                   data=self.move_object)
        Assertions.assert_json_value_by_name(move_new, 'success', True, 'Создание направления завершилось неуспешно')

        # возвращаем значение валидатора
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/b7795021-9e8b-400a-bd04-69de0dff72bc',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                data=self.change_validator_back)
        Assertions.assert_json_value_by_name(change_validator_back, 'success', True,'Изменение валидатора прошло неуспешно')

    @allure.feature("Тесты в массиве на то, что проверяемая дата больше текущей")
    def testBeforeTodayArray(self):
        # сменить параметр для проверки
        new_parameter_in_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/b7795021-9e8b-400a-bd04-69de0dff72bc',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                     data=self.validator_to_array)
        Assertions.assert_json_value_by_name(new_parameter_in_validator, 'success', True,'Изменение валидатора прошло неуспешно')

        # передать текст
        create_text = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                      data=self.create_array)
        Assertions.assert_json_value_by_name(create_text, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать сегодняшний день 2022-08-12 и всё ок
        self.create_array = self.create_array.replace('test_value', f'{datetime.date.today()}')
        create_today_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_date, 'success', True,'Создание направления закончилось ошибкой')
        processId = create_today_date.json()['processId']

        # передать завтрашний день и ошибка
        self.create_array = self.create_array.replace(f'{datetime.date.today()}',f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_tomorrow_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_array)
        Assertions.assert_json_value_by_name(create_tomorrow_date, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать данные в формате 2022-08-12T10:00:00Z с утренним временем сегодняшнего дня и всё ок
        self.create_array = self.create_array.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}',f'{datetime.date.today()}' + 'T00:00:00Z')
        create_today_time_00 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_00, 'success', True,'Создание направления закончилось ошибкой')
        processId_1 = create_today_time_00.json()['processId']

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и получить ошибку
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T00:00:00Z',f'{datetime.date.today()}' + 'T20:00:00Z')
        create_today_time_20 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_20, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')


        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T20:00:00Z',f'{datetime.date.today()}' + 'T03:00:00+03:00')
        create_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_00_3, 'success', True,'Создание направления закончилось ошибкой')
        processId_2 = create_today_time_00_3.json()['processId']

        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T03:00:00+03:00',f'{datetime.date.today()}' + 'T20:00:00+03:00')
        create_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create_array)
        Assertions.assert_json_value_by_name(create_today_time_20_3, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # в запрос moveToStage повторить манипуляции
        self.move_array = self.move_array.replace('example', processId)
        move_array_text = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_text, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать завтрашний день и получить ошибку
        self.move_array = self.move_array.replace('test_value', f'{datetime.date.today() + datetime.timedelta(days=1)}')
        move_tomorrow_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.move_array)
        Assertions.assert_json_value_by_name(move_tomorrow_date, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # передать сегодняшний день и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}',f'{datetime.date.today()}')
        move_today_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_date, 'success', True,'Смена статуса направления закончилась ошибкой')

        # передать данные в формате 2022-08-12T10:00:00Z с вечерним временем сегодняшнего дня и получить ошибку
        replace_values = {processId: processId_1,f'{datetime.date.today()}': f'{datetime.date.today()}' + 'T20:00:00Z'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_today_time_20 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_20, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было утром текущего и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today()}' + 'T20:00:00Z',f'{datetime.date.today()}' + 'T00:00:00Z')
        move_today_time_00 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_00, 'success', True,'Смена статуса направления закончилась ошибкой')

        # повторить манипуляции с 2022-08-12T10:00:00+03:00
        replace_values = {processId_1: processId_2,f'{datetime.date.today()}' + 'T00:00:00Z': f'{datetime.date.today()}' + 'T20:00:00+03:00'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_today_time_20_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_20_3, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # докинуть в этом формате часы сегодняшнего дня, чтобы время было больше текущего и всё ок
        self.move_array = self.move_array.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00',f'{datetime.date.today()}' + 'T03:00:00+03:00')
        move_today_time_00_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move_array)
        Assertions.assert_json_value_by_name(move_today_time_00_3, 'success', True,'Смена статуса направления закончилась ошибкой')

        # изменить в валидаторе на time=false
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/b7795021-9e8b-400a-bd04-69de0dff72bc',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                           data=self.change_array_to_false)
        Assertions.assert_json_value_by_name(change_validator, 'success', True, 'Изменение валидатора прошло неуспешно')

        # передать данные в формате с часами позже текущего за сегодняшний день и не получить ошибку
        create_new = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                     data=self.create_array)
        Assertions.assert_json_value_by_name(create_new, 'success', True, 'Создание направления завершилось неуспешно')
        processId_new = create_new.json()['processId']

        # передать завтрашний день и получить ошибку
        self.create_array = self.create_array.replace(f'{datetime.date.today()}' + 'T20:00:00+03:00',f'{datetime.date.today() + datetime.timedelta(days=1)}')
        create_new_tomorrow = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create_array)
        Assertions.assert_json_value_by_name(create_new_tomorrow, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        # повторить манипуляции с moveToStage
        replace_values = {processId_2: processId_new,f'{datetime.date.today()}' + 'T03:00:00+03:00': f'{datetime.date.today() + datetime.timedelta(days=1)}'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)

        move_new_tomorrow = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                             data=self.move_array)
        Assertions.assert_json_value_by_name(move_new_tomorrow, 'message','Ошибка при проверке даты, которая должна быть меньше текущей','Ошибка о некорректной дате не получена')

        self.move_array = self.move_array.replace(f'{datetime.date.today() + datetime.timedelta(days=1)}',f'{datetime.date.today()}' + 'T20:00:00Z')
        move_new = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},data=self.move_array)
        Assertions.assert_json_value_by_name(move_new, 'success', True, 'Создание направления завершилось неуспешно')

        # возвращаем значение валидатора
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/b7795021-9e8b-400a-bd04-69de0dff72bc',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                data=self.change_validator_back)
        Assertions.assert_json_value_by_name(change_validator_back, 'success', True,'Изменение валидатора прошло неуспешно')

@allure.epic("Проверки Plugins")
class TestDateValidatorCompareDates(BaseCase):

    def setup(self):

        self.create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'1157b7f4-db93-42fd-845d-93214fce9d71','ProcessContext':{'lpu':{'beforeDate':'2022-08-15','afterDate':'2022-08-16'}},'roleContext':{}}"
        self.create_no_before = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'1157b7f4-db93-42fd-845d-93214fce9d71','ProcessContext':{'lpu':{'afterDate':'2022-08-16'}},'roleContext':{}}"
        self.create_equals = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'1157b7f4-db93-42fd-845d-93214fce9d71','ProcessContext':{'lpu':{'beforeDate':'2022-08-16','afterDate':'2022-08-16'}},'roleContext':{}}"
        self.move = "{'processId':'example','transitionId':'50428931-9eba-4eac-aabf-e7f527fbbb68','processContext':{'lpu':{'beforeDate':'2022-08-17','afterDate':'2022-08-16'}},'roleContext':{}}"
        self.move_equals = "{'processId':'example','transitionId':'50428931-9eba-4eac-aabf-e7f527fbbb68','processContext':{'lpu':{'beforeDate':'2022-08-16','afterDate':'2022-08-16'}},'roleContext':{}}"
        self.move_no_after = "{'processId':'example','transitionId':'50428931-9eba-4eac-aabf-e7f527fbbb68','processContext':{'lpu':{'beforeDate':'2022-08-17'}},'roleContext':{}}"

        self.change_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/CompareDates?firstArgument=lpu.beforeDate&secondArgument=lpu.afterDate&isLater=true&time=False","areaId":"bfe35b34-2824-4af6-95c9-49965998f081","messageOnError":"Ошибка при сравнении дат"}'

        self.change_validator_array = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/api/DateValidator/CompareDates?firstArgument=arrayLpu.items.arrayBeforeDate&secondArgument=arrayLpu.items.arrayAfterDate&isLater=false&time=True","areaId":"bfe35b34-2824-4af6-95c9-49965998f081","messageOnError":"Ошибка при сравнении дат"}'

        self.create_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'1157b7f4-db93-42fd-845d-93214fce9d71','ProcessContext':{'arrayLpu':[{'id':'1','arrayBeforeDate':'2022-09-14','arrayAfterDate':'2022-09-14'},{'id':'2','arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-18'}]},'roleContext':{}}"
        self.create_array_no_before = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_date','InitialTransitionId':'1157b7f4-db93-42fd-845d-93214fce9d71','ProcessContext':{'arrayLpu':[{'id':'1','arrayAfterDate':'2022-09-16'},{'id':'2','arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-16'}]},'roleContext':{}}"
        self.move_array = "{'transitionId':'50428931-9eba-4eac-aabf-e7f527fbbb68','processId':'example','processContext':{'arrayLpu':[{'id':'1','arrayBeforeDate':'2022-09-14','arrayAfterDate':'2022-09-14'},{'id':'2','arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-18'}]},'roleContext':{}}"
        self.move_array_no_after = "{'transitionId':'50428931-9eba-4eac-aabf-e7f527fbbb68','processId':'example','processContext':{'arrayLpu':[{'id':'1','arrayBeforeDate':'2022-09-17'},{'id':'2','arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-16'}]},'roleContext':{}}"


        #значение для возврата валидатора к объекту firstArgument=lpu.beforeDate&secondArgument=lpu.afterDate&isLater=false&time=True

    @allure.feature("Тесты на сравнение дат в объекте при time=True и isLater=False")
    def testDateValidatorCompareDatesInObject_timeTrueisLaterFalse(self):

        #проверка с time=True и isLater = false (по умолчанию) - первая дата должна быть больше второй
        #если firstArgument  = secondArgument, то всё ок
        create_equals_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_date = create_equals_date.json()['processId']

        self.create_equals = self.create_equals.replace('2022-08-16', '2022-09-10T11:00:00Z')
        create_equals_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_z = create_equals_time_z.json()['processId']

        self.create_equals = self.create_equals.replace('2022-09-10T11:00:00Z', '2022-09-10T10:00:00+03:00')
        create_equals_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_3 = create_equals_time_3.json()['processId']

        #не передан firstArgument
        create_no_before = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_no_before)
        Assertions.assert_json_value_by_name(create_no_before, 'success',True,'Создание направления закончилось ошибкой')
        processId_no_value = create_no_before.json()['processId']

        #проверить все 3 варианта дат на успех и ошибку
        #передать дату верно и неверно

        create_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_date = create_date.json()['processId']

        self.create = self.create.replace('2022-08-15', '2022-08-17')
        create_date_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_date_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-30T11:00:00Z
        replace_values = {'2022-08-17': '2022-08-17T00:00:00Z','2022-08-16': '2022-08-17T20:00:00Z'}
        self.create = self.multiple_replace(self.create, replace_values)
        create_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_z = create_time_z.json()['processId']


        self.create = self.create.replace('2022-08-17T00:00:00Z', '2022-08-17T21:00:00Z')
        create_time_z_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_z_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-28T10:00:00+03:00
        replace_values = {'2022-08-17T21:00:00Z': '2022-08-17T00:00:00+03:00','2022-08-17T20:00:00Z': '2022-08-17T20:00:00+03:00'}
        self.create = self.multiple_replace(self.create, replace_values)
        create_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_3 = create_time_3.json()['processId']

        self.create = self.create.replace('2022-08-17T00:00:00+03:00', '2022-08-17T21:00:00+03:00')
        create_time_3_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_3_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #проверяем то же поведение в методе moveToStage
        #передать firstArgument  = secondArgument для всех 3 типов даты
        self.move_equals = self.move_equals.replace('example', processId_equals_date)
        move_equals_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_date, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_date: processId_equals_time_z,"2022-08-16": "2022-09-10T11:00:00Z"}
        self.move_equals = self.multiple_replace(self.move_equals, replace_values)
        move_equals_time_z = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_time_z, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_time_z: processId_equals_time_3,"2022-09-10T11:00:00Z": '2022-09-10T10:00:00+03:00'}
        self.move_equals = self.multiple_replace(self.move_equals, replace_values)
        move_equals_time_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_time_3, 'success',True,'Смена статуса направления закончилась ошибкой')

        #не передан secondArgument, но т.к. он уже есть в заявке, то требуется соблюсти правиала проверки
        self.move_no_after = self.move_no_after.replace('example', processId_no_value)
        move_no_after_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_no_after)
        Assertions.assert_json_value_by_name(move_no_after_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #ввести подходящее для проверки значение
        self.move_no_after = self.move_no_after.replace('2022-08-17', '2022-08-15')
        move_no_after_ok = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_no_after)
        Assertions.assert_json_value_by_name(move_no_after_ok, 'success', True,'Смена статуса прошла неуспешно')

        #передать даты
        self.move = self.move.replace('example', processId_date)
        move_date_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_date_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace('2022-08-16', '2022-08-18')
        move_date_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_date_success, 'success', True,'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00Z
        replace_values = {processId_date: processId_time_z,"'beforeDate':'2022-08-17','afterDate':'2022-08-18'": "'beforeDate':'2022-08-17T20:00:00Z','afterDate':'2022-08-17T00:00:00Z'"}
        self.move = self.multiple_replace(self.move, replace_values)
        move_time_z_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace("'beforeDate':'2022-08-17T20:00:00Z','afterDate':'2022-08-17T00:00:00Z'", "'beforeDate':'2022-08-17T00:00:00Z','afterDate':'2022-08-17T20:00:00Z'")
        move_time_z_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_z_success, 'success', True, 'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00+03:00
        replace_values = {processId_time_z: processId_time_3,"'beforeDate':'2022-08-17T00:00:00Z','afterDate':'2022-08-17T20:00:00Z'": "'beforeDate':'2022-08-17T20:00:00+03:00','afterDate':'2022-08-17T00:00:00+03:00'"}
        self.move = self.multiple_replace(self.move, replace_values)
        move_time_3_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_3_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace("'beforeDate':'2022-08-17T20:00:00+03:00','afterDate':'2022-08-17T00:00:00+03:00'", "'beforeDate':'2022-08-17T00:00:00+03:00','afterDate':'2022-08-17T20:00:00+03:00'")
        move_time_3_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_3_success, 'success', True, 'Смена статуса прошла неуспешно')

    @allure.feature("Тесты на сравнение дат в объекте при time=False и Later=True")
    def testDateValidatorCompareDatesInObject_timeFalseisLaterTrue(self):

        #смена значения валидатора на проверку с time=False и isLater = true - вторая дата должна быть больше первой
        isLater_true_time_False = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator.encode('UTF-8'))
        Assertions.assert_json_value_by_name(isLater_true_time_False, 'success', True, 'Обновление валидатора привело к ошибке')

        #если firstArgument  = secondArgument, то всё ок
        create_equals_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_date = create_equals_date.json()['processId']

        self.create_equals = self.create_equals.replace("'beforeDate':'2022-09-10','afterDate':'2022-09-10'", "'beforeDate':'2022-09-10T11:00:00Z','afterDate':'2022-09-10T20:00:00Z'")
        create_equals_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_z = create_equals_time_z.json()['processId']

        self.create_equals = self.create_equals.replace("'beforeDate':'2022-09-10T11:00:00Z','afterDate':'2022-09-10T20:00:00Z'", "'beforeDate':'2022-09-10T10:00:00+03:00','afterDate':'2022-09-10T20:00:00+03:00'")
        create_equals_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_equals)
        Assertions.assert_json_value_by_name(create_equals_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_3 = create_equals_time_3.json()['processId']

        #не передан firstArgument
        create_no_before = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_no_before)
        Assertions.assert_json_value_by_name(create_no_before, 'success',True,'Создание направления закончилось ошибкой')
        processId_no_value = create_no_before.json()['processId']

        #проверить все 3 варианта дат на успех и ошибку
        #передать дату верно и неверно

        create_date_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_date_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.create = self.create.replace('2022-08-15', '2022-08-17')
        create_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_date = create_date.json()['processId']

        #передать в формате 2021-12-30T11:00:00Z
        replace_values = {'2022-08-17': '2022-08-17T00:00:00Z','2022-08-16': '2022-08-16T20:00:00Z'}
        self.create = self.multiple_replace(self.create, replace_values)
        create_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_z = create_time_z.json()['processId']


        self.create = self.create.replace('2022-08-17T00:00:00Z', '2022-08-15T20:00:00Z')
        create_time_z_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_z_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-28T10:00:00+03:00
        replace_values = {'2022-08-15T20:00:00Z': '2022-08-17T00:00:00+03:00','2022-08-16T20:00:00Z': '2022-08-16T20:00:00+03:00'}
        self.create = self.multiple_replace(self.create, replace_values)
        create_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_3 = create_time_3.json()['processId']

        self.create = self.create.replace('2022-08-16T20:00:00+03:00', '2022-08-18T21:00:00+03:00')
        create_time_3_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_time_3_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #проверяем то же поведение в методе moveToStage
        #передать firstArgument  = secondArgument для всех 3 типов даты
        self.move_equals = self.move_equals.replace('example', processId_equals_date)
        move_equals_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_date, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_date: processId_equals_time_z,"2022-08-16": "2022-09-10T11:00:00Z"}
        self.move_equals = self.multiple_replace(self.move_equals, replace_values)
        move_equals_time_z = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_time_z, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_time_z: processId_equals_time_3,"2022-09-10T11:00:00Z": '2022-09-10T10:00:00+03:00'}
        self.move_equals = self.multiple_replace(self.move_equals, replace_values)
        move_equals_time_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_equals)
        Assertions.assert_json_value_by_name(move_equals_time_3, 'success',True,'Смена статуса направления закончилась ошибкой')

        #не передан secondArgument, но т.к. он уже есть в заявке, то требуется соблюсти правиала проверки
        replace_values = {'example': processId_no_value,"2022-08-17": '2022-08-15'}
        self.move_no_after = self.multiple_replace(self.move_no_after, replace_values)
        move_no_after_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_no_after)
        Assertions.assert_json_value_by_name(move_no_after_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #ввести подходящее для проверки значение
        self.move_no_after = self.move_no_after.replace('2022-08-15', '2022-08-17')
        move_no_after_ok = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_no_after)
        Assertions.assert_json_value_by_name(move_no_after_ok, 'success', True,'Смена статуса прошла неуспешно')

        #передать даты
        replace_values = {'example': processId_date,'2022-08-16': '2022-08-18'}
        self.move = self.multiple_replace(self.move, replace_values)
        move_date_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_date_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace('2022-08-18', '2022-08-16')
        move_date_ok = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_date_ok, 'success', True,'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00Z
        replace_values = {processId_date: processId_time_z,"'beforeDate':'2022-08-17','afterDate':'2022-08-16'": "'beforeDate':'2022-08-17T20:00:00Z','afterDate':'2022-08-18T00:00:00Z'"}
        self.move = self.multiple_replace(self.move, replace_values)
        move_time_z_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace("'beforeDate':'2022-08-17T20:00:00Z','afterDate':'2022-08-18T00:00:00Z'", "'beforeDate':'2022-08-17T00:00:00Z','afterDate':'2022-08-16T20:00:00Z'")
        move_time_z_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_z_success, 'success', True, 'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00+03:00
        replace_values = {processId_time_z: processId_time_3,"'beforeDate':'2022-08-17T00:00:00Z','afterDate':'2022-08-16T20:00:00Z'": "'beforeDate':'2022-08-16T20:00:00+03:00','afterDate':'2022-08-17T00:00:00+03:00'"}
        self.move = self.multiple_replace(self.move, replace_values)
        move_time_3_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_3_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move = self.move.replace("'beforeDate':'2022-08-16T20:00:00+03:00','afterDate':'2022-08-17T00:00:00+03:00'", "'beforeDate':'2022-08-17T00:00:00+03:00','afterDate':'2022-08-16T20:00:00+03:00'")
        move_time_3_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_time_3_success, 'success', True, 'Смена статуса прошла неуспешно')

        #вернуть значение валидатора назад
        self.change_validator = self.change_validator.replace("isLater=true&time=False", "isLater=false&time=True")
        isLater_false_time_True = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator.encode('UTF-8'))
        Assertions.assert_json_value_by_name(isLater_false_time_True, 'success', True, 'Обновление валидатора привело к ошибке')

    @allure.feature("Тесты на сравнение дат в массиве при time=True и isLater=False")
    def testDateValidatorCompareDatesInArray_timeTrueisLaterFalse(self):

        validator_to_array = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator_array.encode('UTF-8'))
        Assertions.assert_json_value_by_name(validator_to_array, 'success', True, 'Обновление валидатора привело к ошибке')

        #проверка с time=True и isLater = false (по умолчанию) - первая дата должна быть больше второй
        #если firstArgument  = secondArgument, то всё ок - переданы в первом элементе массива
        create_equals_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_date = create_equals_date.json()['processId']

        self.create_array = self.create_array.replace('2022-09-14', '2022-09-10T11:00:00Z')
        create_equals_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_z = create_equals_time_z.json()['processId']

        self.create_array = self.create_array.replace('2022-09-10T11:00:00Z', '2022-09-10T10:00:00+03:00')
        create_equals_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_3 = create_equals_time_3.json()['processId']

        #не передан firstArgument
        create_no_before = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array_no_before)
        Assertions.assert_json_value_by_name(create_no_before, 'success',True,'Создание направления закончилось ошибкой')
        processId_no_value = create_no_before.json()['processId']

        #проверить все 3 варианта дат на успех и ошибку
        #передать дату неверно во 2 элементе массива
        replace_values = {"'arrayBeforeDate':'2022-09-10T10:00:00+03:00'": "'arrayBeforeDate':'2022-08-17'", "'arrayAfterDate':'2022-09-10T10:00:00+03:00'": "'arrayAfterDate':'2022-08-16'"}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_date_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_date_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-30T11:00:00Z
        replace_values = {'2022-08-17': '2022-08-17T00:00:00Z','2022-08-16': '2022-08-17T20:00:00Z'}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_z = create_time_z.json()['processId']


        self.create_array = self.create_array.replace('2022-08-17T00:00:00Z', '2022-08-17T21:00:00Z')
        create_time_z_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-28T10:00:00+03:00
        replace_values = {'2022-08-17T21:00:00Z': '2022-08-17T00:00:00+03:00','2022-08-17T20:00:00Z': '2022-08-17T20:00:00+03:00'}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_3 = create_time_3.json()['processId']

        create_time_3_additional = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                        data=self.create_array)
        processId_time_3_additional = create_time_3_additional.json()['processId']

        self.create_array = self.create_array.replace('2022-08-17T00:00:00+03:00', '2022-08-17T21:00:00+03:00')
        create_time_3_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_3_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #проверяем то же поведение в методе moveToStage
        #передать firstArgument  = secondArgument для всех 3 типов даты
        self.move_array = self.move_array.replace('example', processId_equals_date)
        move_equals_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_date, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_date: processId_equals_time_z,"2022-09-14": "2022-09-10T11:00:00Z"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_equals_time_z = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_time_z, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_time_z: processId_equals_time_3,"2022-09-10T11:00:00Z": '2022-09-10T10:00:00+03:00'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_equals_time_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_time_3, 'success',True,'Смена статуса направления закончилась ошибкой')

        #не передан secondArgument, но т.к. он уже есть в заявке, то требуется соблюсти правиала проверки
        self.move_array_no_after = self.move_array_no_after.replace('example', processId_no_value)
        move_no_after_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array_no_after)
        Assertions.assert_json_value_by_name(move_no_after_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #ввести подходящее для проверки значение
        self.move_array_no_after = self.move_array_no_after.replace("'id':'1','arrayBeforeDate':'2022-09-17'", "'id':'1','arrayBeforeDate':'2022-09-15'")
        move_no_after_ok = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array_no_after)
        Assertions.assert_json_value_by_name(move_no_after_ok, 'success', True,'Смена статуса прошла неуспешно')

        #передать даты
        replace_values = {processId_equals_time_3: processId_time_z,"'arrayBeforeDate':'2022-08-15'": "'arrayBeforeDate':'2022-08-19'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_date_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_date_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move_array = self.move_array.replace('2022-08-19', '2022-08-15')
        move_date_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_date_success, 'success', True,'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00Z
        replace_values = {processId_time_z: processId_time_3, "'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-18'": "'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-17T00:00:00Z'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_time_z_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move_array = self.move_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-17T00:00:00Z'", "'arrayBeforeDate':'2022-08-17T00:00:00Z','arrayAfterDate':'2022-08-17T20:00:00Z'")
        move_time_z_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_z_success, 'success', True, 'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00+03:00
        replace_values = {processId_time_3: processId_time_3_additional,"'arrayBeforeDate':'2022-08-17T00:00:00Z','arrayAfterDate':'2022-08-17T20:00:00Z'": "'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-17T00:00:00+03:00'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_time_3_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_3_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move_array = self.move_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-17T00:00:00+03:00'", "'arrayBeforeDate':'2022-08-17T00:00:00+03:00','arrayAfterDate':'2022-08-17T20:00:00+03:00'")
        move_time_3_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_3_success, 'success', True, 'Смена статуса прошла неуспешно')

        #вернуть валидатор в исходное состояние
        self.change_validator_array = self.change_validator_array.replace("firstArgument=arrayLpu.items.arrayBeforeDate&secondArgument=arrayLpu.items.arrayAfterDate", "firstArgument=lpu.beforeDate&secondArgument=lpu.afterDate")
        validator_to_object = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator.encode('UTF-8'))
        Assertions.assert_json_value_by_name(validator_to_object, 'success', True, 'Обновление валидатора привело к ошибке')

    @allure.feature("Тесты на сравнение дат в массиве при time=False и isLater=True")
    def testDateValidatorCompareDatesInArray_timeFalseisLaterTrue(self):

        self.change_validator_array = self.change_validator_array.replace('isLater=false&time=True', 'isLater=true&time=False')
        validator_to_array = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator_array.encode('UTF-8'))
        Assertions.assert_json_value_by_name(validator_to_array, 'success', True, 'Обновление валидатора привело к ошибке')

        #проверка с time=False и isLater = true - первая дата должна быть меньше второй
        #если firstArgument  = secondArgument, то всё ок - переданы в первом элементе массива
        self.create_array = self.create_array.replace("'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-18'", "'arrayBeforeDate':'2022-08-18','arrayAfterDate':'2022-08-15'")
        create_equals_date = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_date, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_date = create_equals_date.json()['processId']

        self.create_array = self.create_array.replace('2022-09-14', '2022-09-10T11:00:00Z')
        create_equals_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_z = create_equals_time_z.json()['processId']

        self.create_array = self.create_array.replace('2022-09-10T11:00:00Z', '2022-09-10T10:00:00+03:00')
        create_equals_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_equals_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_equals_time_3 = create_equals_time_3.json()['processId']

        #не передан firstArgument
        self.create_array_no_before = self.create_array_no_before.replace("'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-16'", "'arrayBeforeDate':'2022-08-16','arrayAfterDate':'2022-08-15'")
        create_no_before = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array_no_before)
        Assertions.assert_json_value_by_name(create_no_before, 'success',True,'Создание направления закончилось ошибкой')
        processId_no_value = create_no_before.json()['processId']

        #проверить все 3 варианта дат на успех и ошибку
        #передать дату неверно во 2 элементе массива
        replace_values = {"'arrayBeforeDate':'2022-09-10T10:00:00+03:00'": "'arrayBeforeDate':'2022-08-16'", "'arrayAfterDate':'2022-09-10T10:00:00+03:00'": "'arrayAfterDate':'2022-08-17'"}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_date_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_date_error, 'message','Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-30T11:00:00Z
        replace_values = {'2022-08-17': '2022-08-17T00:00:00Z','2022-08-16': '2022-08-17T20:00:00Z'}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_time_z = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_z = create_time_z.json()['processId']

        #проверка что при передаче часов они не сравниваются и успешно создается заявка
        self.create_array = self.create_array.replace('2022-08-17T00:00:00Z', '2022-08-17T20:30:00Z')
        create_time_z_no_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z_no_error, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_z_no_error = create_time_z_no_error.json()['processId']

        #ошибка, если дата неверная
        self.create_array = self.create_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-17T20:30:00Z'", "'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-18T20:30:00Z'")
        create_time_z_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать в формате 2021-12-28T10:00:00+03:00
        replace_values = {'2022-08-18T20:30:00Z': '2022-08-17T00:00:00+03:00','2022-08-17T20:00:00Z': '2022-08-17T20:00:00+03:00'}
        self.create_array = self.multiple_replace(self.create_array, replace_values)
        create_time_3 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_3, 'success',True,'Создание направления закончилось ошибкой')
        processId_time_3 = create_time_3.json()['processId']

        # проверка что при передаче часов они не сравниваются и успешно создается заявка
        self.create_array = self.create_array.replace('2022-08-17T00:00:00+03:00', '2022-08-17T20:30:00+03:00')
        create_time_3_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_3_error, 'success',True,'Создание направления закончилось ошибкой')

        #ошибка, если дата неверная
        self.create_array = self.create_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-17T20:30:00+03:00'", "'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-18T20:30:00+03:00'")
        create_time_z_error = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #проверяем то же поведение в методе moveToStage
        #передать firstArgument  = secondArgument для всех 3 типов даты
        replace_values = {'example': processId_equals_date,"'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-18'": "'arrayBeforeDate':'2022-08-19','arrayAfterDate':'2022-08-18'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_equals_date = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_date, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_date: processId_equals_time_z,"2022-09-14": "2022-09-10T11:00:00Z"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_equals_time_z = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_time_z, 'success',True,'Смена статуса направления закончилась ошибкой')

        replace_values = {processId_equals_time_z: processId_equals_time_3,"2022-09-10T11:00:00Z": '2022-09-10T10:00:00+03:00'}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_equals_time_3 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_equals_time_3, 'success',True,'Смена статуса направления закончилась ошибкой')

        #не передан secondArgument, но т.к. он уже есть в заявке, то требуется соблюсти правиала проверки
        replace_values = {'example': processId_no_value,"'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-16'": "'arrayBeforeDate':'2022-08-15','arrayAfterDate':'2022-08-14'",
                          "'arrayBeforeDate':'2022-09-17'": "'arrayBeforeDate':'2022-09-15'"}
        self.move_array_no_after = self.multiple_replace(self.move_array_no_after, replace_values)
        move_no_after_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array_no_after)
        Assertions.assert_json_value_by_name(move_no_after_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #ввести подходящее для проверки значение
        self.move_array_no_after = self.move_array_no_after.replace("'arrayBeforeDate':'2022-09-15'", "'arrayBeforeDate':'2022-09-17'")
        move_no_after_ok = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array_no_after)
        Assertions.assert_json_value_by_name(move_no_after_ok, 'success', True,'Смена статуса прошла неуспешно')

        #передать даты
        replace_values = {processId_equals_time_3: processId_time_z,"'arrayBeforeDate':'2022-08-19'": "'arrayBeforeDate':'2022-08-17'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_date_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_date_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move_array = self.move_array.replace('2022-08-17', '2022-08-19')
        move_date_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_date_success, 'success', True,'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00Z
        replace_values = {processId_time_z: processId_time_3, "'arrayBeforeDate':'2022-08-19','arrayAfterDate':'2022-08-18'": "'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-18T20:30:00Z'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_time_z_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_z_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        #передать время и проверить что часы не учитываются
        self.move_array = self.move_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-18T20:30:00Z'", "'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-17T20:30:00Z'")
        move_time_z_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_z_success, 'success', True, 'Смена статуса прошла неуспешно')

        #передать в формате 2022-08-17T00:00:00+03:00
        replace_values = {processId_time_3: processId_time_z_no_error,"'arrayBeforeDate':'2022-08-17T20:00:00Z','arrayAfterDate':'2022-08-17T20:30:00Z'": "'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-18T10:00:00+03:00'"}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_time_3_error = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_3_error, 'message', 'Ошибка при сравнении дат','Ожидаемая ошибка сравнения дат не получена')

        self.move_array = self.move_array.replace("'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-18T10:00:00+03:00'", "'arrayBeforeDate':'2022-08-17T20:00:00+03:00','arrayAfterDate':'2022-08-17T10:00:00+03:00'")
        move_time_3_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_time_3_success, 'success', True, 'Смена статуса прошла неуспешно')

        #вернуть валидатор в исходное состояние
        self.change_validator_array = self.change_validator_array.replace("firstArgument=arrayLpu.items.arrayBeforeDate&secondArgument=arrayLpu.items.arrayAfterDate&isLater=true&time=False", "firstArgument=lpu.beforeDate&secondArgument=lpu.afterDate&isLater=false&time=True")
        validator_to_object = MyRequests.post(f'/tm-core/api/Commands/UpdateExternalValidator/321a579c-0eb7-499e-acda-e1490d2f4b1b', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                  data=self.change_validator_array.encode('UTF-8'))
        Assertions.assert_json_value_by_name(validator_to_object, 'success', True, 'Обновление валидатора привело к ошибке')

@allure.epic("Проверки Plugins")
class TestValidatePhone(BaseCase):

    def setup(self):

        self.create_object = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_phone','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'serviceRequest':{'phone':'+7999111222'}},'roleContext':{}}"
        self.move_object = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'serviceRequest':{'phone':'+7999111222'}},'roleContext':{}}"

        self.change_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/Validators/ValidatePhone?argument=arrayLpu.items.phone","messageOnError":"Ошибка при проверке формата телефона","areaId":"bfe35b34-2824-4af6-95c9-49965998f081"}'.encode('UTF-8')
        self.comeback_validator = '{"url":"http://r78-test.zdrav.netrika.ru/tm-plugins/Validators/ValidatePhone?argument=serviceRequest.phone","messageOnError":"Ошибка при проверке формата телефона","areaId":"bfe35b34-2824-4af6-95c9-49965998f081"}'.encode('UTF-8')

        self.create_array = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check_phone','InitialTransitionId':'35b8a113-d272-419b-9748-68020bd00ff4','ProcessContext':{'arrayLpu':[{'id':'1','phone':'+71111111111'},{'id':'2','phone':'+7222222222'}]},'roleContext':{}}"
        self.move_array = "{'processId':'example','transitionId':'9fc9da80-2e7d-4d6c-926e-b4861d103f66','processContext':{'arrayLpu':[{'id':'1','phone':'+71111111111'},{'id':'2','phone':'+7222222222'}]},'roleContext':{}}"

    @allure.feature("Тесты в объекте на то, что переданный телефон соответствует формату")
    def testPhoneFormatObject(self):

        #передать меньше чисел, чем должно быть
        create_object_less_value = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_less_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать больше чисел, чем должно быть
        self.create_object = self.create_object.replace('+7999111222', '+799911122222')
        create_object_more_value = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_more_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать не с 7 в начале
        self.create_object = self.create_object.replace('+799911122222', '+11111111111')
        create_object_no_7 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_no_7, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать без +
        self.create_object = self.create_object.replace('+11111111111', '71111111111')
        create_object_no_plus = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_no_plus, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с пробелами
        self.create_object = self.create_object.replace('71111111111', '+7 999 222 33 44')
        create_object_with_space = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_with_space, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с тире и скобками
        self.create_object = self.create_object.replace('+7 999 222 33 44', '+7 (999) 111-55-43')
        create_object_with_symbols = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_with_symbols, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать текст
        self.create_object = self.create_object.replace('+7 (999) 111-55-43', 'test')
        create_object_with_txt = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_with_txt, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать верный формат
        self.create_object = self.create_object.replace('test', '+71111111111')
        create_object_correct = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object_correct, 'success',True,'Создание направления завершилось неуспешно')
        processId = create_object_correct.json()['processId']

        #не передан проверяемый параметр
        self.create_object = self.create_object.replace("'phone':'+71111111111'", ' ')
        create_object = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_object)
        Assertions.assert_json_value_by_name(create_object, 'success',True,'Создание направления завершилось неуспешно')
        processId_empty = create_object.json()['processId']

        #повторить всё то же самое, только для смены статуса

        #передать меньше чисел, чем должно быть
        self.move_object = self.move_object.replace('example', processId)
        move_object_less_value = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_less_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать больше чисел, чем должно быть
        self.move_object = self.move_object.replace('+7999111222', '+799911122222')
        move_object_more_value = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_more_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать не с 7 в начале
        self.move_object = self.move_object.replace('+799911122222', '+11111111111')
        move_object_no_7 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_no_7, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать без +
        self.move_object = self.move_object.replace('+11111111111', '71111111111')
        move_object_no_plus = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_no_plus, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с пробелами
        self.move_object = self.move_object.replace('71111111111', '+7 999 222 33 44')
        move_object_with_space = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_with_space, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с тире и скобками
        self.move_object = self.move_object.replace('+7 999 222 33 44', '+7 (999) 111-55-43')
        move_object_with_symbols = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_with_symbols, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать текст
        self.move_object = self.move_object.replace('+7 (999) 111-55-43', 'test')
        move_object_with_txt = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_with_txt, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать верный формат
        self.move_object = self.move_object.replace('test', '+71111111111')
        move_object_correct = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object_correct, 'success',True,'Смена статуса направления завершилась неуспешно')

        #не передан проверяемый параметр
        replace_values = {processId: processId_empty,"'phone':'+71111111111'": ' '}
        self.move_object = self.multiple_replace(self.move_object, replace_values)
        move_object = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_object)
        Assertions.assert_json_value_by_name(move_object, 'success',True,'Смена статуса направления завершилась неуспешно')

    @allure.feature("Тесты в массиве на то, что переданный телефон соответствует формату")
    def testPhoneFormatArray(self):

        #смена валидатора на массив
        change_validator = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/1701c425-9819-4800-8e69-f7e7faca6ec4',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                     data=self.change_validator)
        Assertions.assert_json_value_by_name(change_validator, 'success', True,'Изменение валидатора прошло неуспешно')

        #передать меньше чисел, чем должно быть
        create_array_less_value = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_less_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать больше чисел, чем должно быть
        self.create_array = self.create_array.replace('+7222222222', '+722222222222')
        create_array_more_value = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_more_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать не с 7 в начале
        self.create_array = self.create_array.replace('+722222222222', '+11111111111')
        create_array_no_7 = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_no_7, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать без +
        self.create_array = self.create_array.replace('+11111111111', '72222222222')
        create_array_no_plus = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_no_plus, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с пробелами
        self.create_array = self.create_array.replace('72222222222', '+7 999 222 33 44')
        create_array_with_space = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_with_space, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с тире и скобками
        self.create_array = self.create_array.replace('+7 999 222 33 44', '+7 (999) 111-55-43')
        create_array_with_symbols = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_with_symbols, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать текст
        self.create_array = self.create_array.replace('+7 (999) 111-55-43', 'test')
        create_array_with_txt = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_with_txt, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать верный формат
        self.create_array = self.create_array.replace('test', '+72222222222')
        create_array_correct = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array_correct, 'success',True,'Создание направления завершилось неуспешно')
        processId = create_array_correct.json()['processId']

        #не передан проверяемый параметр
        self.create_array = self.create_array.replace("'phone':'+72222222222'", ' ')
        create_array = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_array)
        Assertions.assert_json_value_by_name(create_array, 'success',True,'Создание направления завершилось неуспешно')
        processId_empty = create_array.json()['processId']

        #повторить всё то же самое, только для смены статуса

        #передать меньше чисел, чем должно быть
        self.move_array = self.move_array.replace('example', processId)
        move_array_less_value = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_less_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать больше чисел, чем должно быть
        self.move_array = self.move_array.replace('+7222222222', '+799911122222')
        move_array_more_value = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_more_value, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать не с 7 в начале
        self.move_array = self.move_array.replace('+799911122222', '+22222222222')
        move_array_no_7 = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_no_7, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать без +
        self.move_array = self.move_array.replace('+22222222222', '72222222222')
        move_array_no_plus = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_no_plus, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с пробелами
        self.move_array = self.move_array.replace('72222222222', '+7 999 222 33 44')
        move_array_with_space = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_with_space, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать с тире и скобками
        self.move_array = self.move_array.replace('+7 999 222 33 44', '+7 (999) 111-55-43')
        move_array_with_symbols = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_with_symbols, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать текст
        self.move_array = self.move_array.replace('+7 (999) 111-55-43', 'test')
        move_array_with_txt = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_with_txt, 'message','Ошибка при проверке формата телефона','Ожидаемая ошибка проверки телефона не получена')

        #передать верный формат
        self.move_array = self.move_array.replace('test', '+72222222222')
        move_array_correct = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array_correct, 'success',True,'Смена статуса направления завершилась неуспешно')

        #не передан проверяемый параметр
        replace_values = {processId: processId_empty,"'phone':'+72222222222'": ' '}
        self.move_array = self.multiple_replace(self.move_array, replace_values)
        move_array = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move_array)
        Assertions.assert_json_value_by_name(move_array, 'success',True,'Смена статуса направления завершилась неуспешно')

        #вернуть валидатор назад
        change_validator_back = MyRequests.post('/tm-core/api/Commands/UpdateExternalValidator/1701c425-9819-4800-8e69-f7e7faca6ec4',headers={'Authorization': f'{config.token_tm_core}', 'Content-Type': 'application/json-patch+json'},
                                                     data=self.comeback_validator)
        Assertions.assert_json_value_by_name(change_validator_back, 'success', True,'Изменение валидатора прошло неуспешно')

@allure.epic("Проверки Plugins")
class TestCheckSnils(BaseCase):

    def setup(self):

        self.create = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check SNILS','InitialTransitionId':'1e51323e-bfaa-4657-a7f7-e459daf634da','ProcessContext':{'Doctors':[{'id':'1','SNILS':'11111111111','lpuId':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682','position':'45'}]},'roleContext':{}}"
        self.create_empty = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check SNILS','InitialTransitionId':'1e51323e-bfaa-4657-a7f7-e459daf634da','ProcessContext':{},'roleContext':{}}"
        self.create_no_snils = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check SNILS','InitialTransitionId':'1e51323e-bfaa-4657-a7f7-e459daf634da','ProcessContext':{'Doctors':[{'id':'1','lpuId':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682','position':'45'}]},'roleContext':{}}"
        self.create_no_lpuid = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check SNILS','InitialTransitionId':'1e51323e-bfaa-4657-a7f7-e459daf634da','ProcessContext':{'Doctors':[{'id':'1','SNILS':'54248927312','position':'45'}]},'roleContext':{}}"
        self.create_no_position = "{'WorkflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','Name':'Check SNILS','InitialTransitionId':'1e51323e-bfaa-4657-a7f7-e459daf634da','ProcessContext':{'Doctors':[{'id':'1','SNILS':'54248927312','lpuId':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682'}]},'roleContext':{}}"

        self.move = "{'processId':'example','transitionId':'b1714fb9-d1e6-42fb-b496-84e3a2e82783','processContext':{'Doctors':[{'id':'1','SNILS':'11111111111','lpuId':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682','position':'45'}]},'roleContext':{}}"
        self.move_empty = "{'processId':'example','transitionId':'b1714fb9-d1e6-42fb-b496-84e3a2e82783','processContext':{},'roleContext':{}}"

    @allure.feature("Тесты на то, что переданные данные СНИЛСа соответствуют данным из НСИ")
    def testCheckSnils(self):

        #не передан массив Doctors как таковой
        create_without_data = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create_empty)
        Assertions.assert_json_value_by_name(create_without_data, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан неверный SNILS или не передан сам параметр
        create_incorrect_snils = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_incorrect_snils, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        create_no_snils = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_no_snils)
        Assertions.assert_json_value_by_name(create_no_snils, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан неверный lpuId или не передан сам параметр
        replace_values = {'11111111111': '54248927312', '3b4b37cd-ef0f-4017-9eb4-2fe49142f682': '3b4b37cd-ef0f-4017-9eb4-2fe49142f683'}
        self.create = self.multiple_replace(self.create, replace_values)

        create_incorrect_lpuid = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create)
        Assertions.assert_json_value_by_name(create_incorrect_lpuid, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        create_no_lpuid = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.create_no_lpuid)
        Assertions.assert_json_value_by_name(create_no_lpuid, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан неверный position или не передан сам параметр
        replace_values = {'3b4b37cd-ef0f-4017-9eb4-2fe49142f683': '3b4b37cd-ef0f-4017-9eb4-2fe49142f682',"'position':'45'": "'position':'test'"}
        self.create = self.multiple_replace(self.create, replace_values)

        create_incorrect_position = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.create)
        Assertions.assert_json_value_by_name(create_incorrect_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        create_no_position = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.create_no_position)
        Assertions.assert_json_value_by_name(create_no_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан SNILS от другого врача
        replace_values = {"'position':'test'": "'position':'45'",'54248927312': '48368377143'}
        self.create = self.multiple_replace(self.create, replace_values)

        create_another_snils = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.create)
        Assertions.assert_json_value_by_name(create_another_snils, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # передан lpuId от другого врача
        replace_values = {'3b4b37cd-ef0f-4017-9eb4-2fe49142f682': '6c34dc18-cab0-4e53-aba8-cea197f0ab5e', '48368377143': '54248927312'}
        self.create = self.multiple_replace(self.create, replace_values)

        create_another_lpuid = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create)
        Assertions.assert_json_value_by_name(create_another_lpuid, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # переданы lpuId и position от другого врача
        self.create = self.create.replace("'position':'45'", "'position':'1'")
        create_another_lpuid_position = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create)
        Assertions.assert_json_value_by_name(create_another_lpuid_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # передан position от другого врача
        self.create = self.create.replace('6c34dc18-cab0-4e53-aba8-cea197f0ab5e', '3b4b37cd-ef0f-4017-9eb4-2fe49142f682')
        create_another_position = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create)
        Assertions.assert_json_value_by_name(create_another_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #все параметры переданы верно и направление успешно создается
        self.create = self.create.replace("'position':'1'", "'position':'45'")
        create_success = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create)
        Assertions.assert_json_value_by_name(create_success, 'success', True, 'Создание направления завершилось с ошибкой')
        processId = create_success.json()['processId']

        create_success_for_empty = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.create)
        Assertions.assert_json_value_by_name(create_success_for_empty, 'success', True, 'Создание направления завершилось с ошибкой')
        processId_empty = create_success_for_empty.json()['processId']

        #повторить для moveToStage
        self.move = self.move.replace('example', processId)
        self.move_empty = self.move_empty.replace('example', processId_empty)

        #т.к. в  processContext заявки данные поля уже есть, то если их не передать, то ошибки не будет
        move_success_empty = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                       data=self.move_empty)
        Assertions.assert_json_value_by_name(move_success_empty, 'success', True,'Создание направления завершилось с ошибкой')

        #передан неверный SNILS
        move_incorrect_snils = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_incorrect_snils, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан неверный lpuId
        replace_values = {'11111111111': '54248927312', '3b4b37cd-ef0f-4017-9eb4-2fe49142f682': '3b4b37cd-ef0f-4017-9eb4-2fe49142f683'}
        self.move = self.multiple_replace(self.move, replace_values)
        move_incorrect_lpuid = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                            data=self.move)
        Assertions.assert_json_value_by_name(move_incorrect_lpuid, 'message','Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан неверный position
        replace_values = {'3b4b37cd-ef0f-4017-9eb4-2fe49142f683': '3b4b37cd-ef0f-4017-9eb4-2fe49142f682',"'position':'45'": "'position':'test'"}
        self.move = self.multiple_replace(self.move, replace_values)
        move_incorrect_position = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                 data=self.move)
        Assertions.assert_json_value_by_name(move_incorrect_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #передан SNILS от другого врача
        replace_values = {"'position':'test'": "'position':'45'",'54248927312': '48368377143'}
        self.move = self.multiple_replace(self.move, replace_values)
        move_another_snils = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                          data=self.move)
        Assertions.assert_json_value_by_name(move_another_snils, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # передан lpuId от другого врача
        replace_values = {'3b4b37cd-ef0f-4017-9eb4-2fe49142f682': '6c34dc18-cab0-4e53-aba8-cea197f0ab5e', '48368377143': '54248927312'}
        self.move = self.multiple_replace(self.move, replace_values)
        move_another_lpuid = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move)
        Assertions.assert_json_value_by_name(move_another_lpuid, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # переданы lpuId и position от другого врача
        self.move = self.move.replace("'position':'45'", "'position':'1'")
        move_another_lpuid_position = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move)
        Assertions.assert_json_value_by_name(move_another_lpuid_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        # передан position от другого врача
        self.move = self.move.replace('6c34dc18-cab0-4e53-aba8-cea197f0ab5e', '3b4b37cd-ef0f-4017-9eb4-2fe49142f682')
        move_another_position = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move)
        Assertions.assert_json_value_by_name(move_another_position, 'message', 'Ошибка при проверке СНИЛС','Ожидаемая ошибка проверки СНИЛС не получена')

        #все параметры переданы верно и направление успешно создается
        self.move = self.move.replace("'position':'1'", "'position':'45'")
        move_success = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                               data=self.move)
        Assertions.assert_json_value_by_name(move_success, 'success', True, 'Создание направления завершилось с ошибкой')

@allure.epic("Проверки Plugins")
class TestCheckBirthDate(BaseCase):

    def setup(self):

        self.date_today_14 = datetime.date.today().replace(year=int(datetime.datetime.now().year) - 14)
        self.date_today_18 = datetime.date.today().replace(year=int(datetime.datetime.now().year) - 18)

        self.create = "{'initialTransitionId':'650942a4-2ed6-404f-b77d-ff1a51a31d8a','name':'Test birthDate','workflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','processContext':{'patient':{'birthDate':'day'},'observation':{'ageType':'1'}},'roleContext':{}}"
        self.create_empty_context = "{'initialTransitionId':'650942a4-2ed6-404f-b77d-ff1a51a31d8a','name':'Test birthDate','workflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','processContext':{},'roleContext':{}}"
        self.create_no_ageType = "{'initialTransitionId':'650942a4-2ed6-404f-b77d-ff1a51a31d8a','name':'Test birthDate','workflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','processContext':{'patient':{'birthDate':'day'}},'roleContext':{}}"
        self.create_no_birthDate = "{'initialTransitionId':'650942a4-2ed6-404f-b77d-ff1a51a31d8a','name':'Test birthDate','workflowId':'09872eef-6180-4f5f-9137-c33ce60ad416','processContext':{'observation':{'ageType':'1'}},'roleContext':{}}"

        self.move = "{'transitionId':'fea3e507-6b4b-46c3-9200-b88dd9da9595','processId':'example','processContext':{'patient':{'birthDate':'day'},'observation':{'ageType':'1'}},'roleContext':{}}"
        self.move_empty_context = "{'transitionId':'fea3e507-6b4b-46c3-9200-b88dd9da9595','processId':'example','processContext':{},'roleContext':{}}"

    @allure.feature("Тесты на соответствие параметров ageType и birthDate")
    def testCheckBirthDate(self):

        # передать неверное значение в дату
        create_wrong_birthDate = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_wrong_birthDate, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст больше 14
        self.create = self.create.replace('day', f'{self.date_today_14 + datetime.timedelta(days=-1)}')
        create_1_more_14 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_1_more_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст равный 14
        self.create = self.create.replace(f'{self.date_today_14 + datetime.timedelta(days=-1)}', f'{self.date_today_14}')
        create_1_equals_14 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_1_equals_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст меньше 14
        self.create = self.create.replace(f'{self.date_today_14}', f'{self.date_today_14 + datetime.timedelta(days=1)}')
        create_1_less_14 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_1_less_14, 'success', True, 'Создание направления завершилось неуспешно')
        processId_14 = create_1_less_14.json()['processId']

        # передать неверное значение в ageType
        self.create = self.create.replace("'ageType':'1'", "'ageType':'type'")
        create_wrong_ageType = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_wrong_ageType, 'success', True, 'Создание направления завершилось неуспешно')
        processId_14_ageType = create_wrong_ageType.json()['processId']

        replace_values = {"'ageType':'type'": "'ageType':'2'", f'{self.date_today_14 + datetime.timedelta(days=1)}': f'{self.date_today_14}'}
        self.create = self.multiple_replace(self.create, replace_values)

        # при "ageType": "2" передать возраст равный 14
        create_2_equals_14 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_2_equals_14, 'success', True, 'Создание направления завершилось неуспешно')
        processId_equals_14 = create_2_equals_14.json()['processId']

        #при "ageType": "2" передать возраст между 14 и 18
        self.create = self.create.replace(f'{self.date_today_14}', f'{self.date_today_14 + datetime.timedelta(days=-1)}')
        create_2_between_14_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_2_between_14_18, 'success', True, 'Создание направления завершилось неуспешно')
        processId_between_14_18 = create_2_between_14_18.json()['processId']

        #при "ageType": "2" передать возраст младше 14
        self.create = self.create.replace(f'{self.date_today_14 + datetime.timedelta(days=-1)}', f'{self.date_today_14 + datetime.timedelta(days=1)}')
        create_2_less_14 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_2_less_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "2" передать возраст равный 18
        self.create = self.create.replace(f'{self.date_today_14 + datetime.timedelta(days=1)}', f'{self.date_today_18}')
        create_2_equals_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_2_equals_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "2" передать возраст старше 18
        self.create = self.create.replace(f'{self.date_today_18}', f'{self.date_today_18 + datetime.timedelta(days=-1)}')
        create_2_more_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_2_more_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        self.create = self.create.replace("'ageType':'2'", "'ageType':'3'")

        # при "ageType": "3" передать возраст старше 18
        create_3_more_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_3_more_18, 'success', True, 'Создание направления завершилось неуспешно')
        processId_18 = create_3_more_18.json()['processId']

        # при "ageType": "3" передать возраст равный 18
        self.create = self.create.replace(f'{self.date_today_18 + datetime.timedelta(days=-1)}', f'{self.date_today_18}')
        create_3_equals_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_3_equals_18, 'success', True, 'Создание направления завершилось неуспешно')
        processId_equals_18 = create_3_equals_18.json()['processId']

        # при "ageType": "3" передать возраст младше 18
        self.create = self.create.replace(f'{self.date_today_18}', f'{self.date_today_18 + datetime.timedelta(days=1)}')
        create_3_more_18 = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create)
        Assertions.assert_json_value_by_name(create_3_more_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #не передать параметры ageType и birthDate
        create_empty = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create_empty_context)
        Assertions.assert_json_value_by_name(create_empty, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        # не передать ageType
        self.create_no_ageType = self.create_no_ageType.replace('day', f'{self.date_today_14}')
        create_no_ageType = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create_no_ageType)
        Assertions.assert_json_value_by_name(create_no_ageType, 'success', True, 'Создание направления завершилось неуспешно')
        processId_no_ageType = create_no_ageType.json()['processId']

        # не передать birthDate
        create_no_birthDate = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.create_no_birthDate)
        Assertions.assert_json_value_by_name(create_no_birthDate, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        # повторить в moveToStage
        self.move = self.move.replace('example', processId_14)

        # передать неверное значение в дату
        move_wrong_birthDate = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_wrong_birthDate, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст больше 14
        self.move = self.move.replace('day', f'{self.date_today_14 + datetime.timedelta(days=-1)}')
        move_1_more_14 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_1_more_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст равный 14
        self.move = self.move.replace(f'{self.date_today_14 + datetime.timedelta(days=-1)}', f'{self.date_today_14}')
        move_1_equals_14 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_1_equals_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "1" передать возраст меньше 14
        self.move = self.move.replace(f'{self.date_today_14}', f'{self.date_today_14 + datetime.timedelta(days=1)}')
        move_1_less_14 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_1_less_14, 'success', True, 'Смена статуса направления завершилась неуспешно')

        # передать неверное значение в ageType
        replace_values = {"'ageType':'1'": "'ageType':'type'", processId_14: processId_equals_14}
        self.move = self.multiple_replace(self.move, replace_values)
        move_wrong_ageType = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_wrong_ageType, 'success', True, 'Смена статуса направления завершилась неуспешно')

        replace_values = {"'ageType':'type'": "'ageType':'2'", processId_equals_14: processId_14_ageType}
        self.move = self.multiple_replace(self.move, replace_values)

        # при "ageType": "2" передать возраст меньше 14
        move_2_less_14 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_2_less_14, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "2" передать возраст между 14 и 18
        self.move = self.move.replace(f'{self.date_today_14 + datetime.timedelta(days=1)}', f'{self.date_today_14 + datetime.timedelta(days=-1)}')
        move_2_between_14_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_2_between_14_18, 'success', True, 'Смена статуса направления завершилась ошибкой')

        #при "ageType": "2" передать возраст ровно 14
        replace_values = {f'{self.date_today_14 + datetime.timedelta(days=-1)}': f'{self.date_today_14}', processId_14_ageType: processId_between_14_18}
        self.move = self.multiple_replace(self.move, replace_values)
        move_2_equals_14 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_2_equals_14, 'success', True, 'Смена статуса направления завершилась ошибкой')

        #при "ageType": "2" передать возраст равный 18
        replace_values = {f'{self.date_today_14}': f'{self.date_today_18}', processId_between_14_18: processId_18}
        self.move = self.multiple_replace(self.move, replace_values)
        move_2_equals_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_2_equals_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #при "ageType": "2" передать возраст старше 18
        self.move = self.move.replace(f'{self.date_today_18}', f'{self.date_today_18 + datetime.timedelta(days=-1)}')
        move_2_more_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_2_more_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        self.move = self.move.replace("'ageType':'2'", "'ageType':'3'")

        # при "ageType": "3" передать возраст старше 18
        move_3_more_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_3_more_18, 'success', True, 'Смена статуса направления завершилась ошибкой')

        # при "ageType": "3" передать возраст равный 18
        replace_values = {f'{self.date_today_18 + datetime.timedelta(days=-1)}': f'{self.date_today_18}', processId_18: processId_equals_18}
        self.move = self.multiple_replace(self.move, replace_values)
        move_3_equals_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_3_equals_18, 'success', True, 'Смена статуса направления завершилась ошибкой')

        # при "ageType": "3" передать возраст младше 18
        replace_values = {f'{self.date_today_18}': f'{self.date_today_18 + datetime.timedelta(days=1)}', processId_equals_18: processId_no_ageType}
        self.move = self.multiple_replace(self.move, replace_values)
        move_3_less_18 = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move)
        Assertions.assert_json_value_by_name(move_3_less_18, 'message', 'Пациент не соответствует возрастной категории профиля', 'Ожидаемая ошибка не получена')

        #не передать параметры ageType и birthDate
        self.move_empty_context = self.move_empty_context.replace('example', processId_no_ageType)
        move_empty = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                           data=self.move_empty_context)
        Assertions.assert_json_value_by_name(move_empty, 'success', True, 'Смена статуса направления завершилась ошибкой')