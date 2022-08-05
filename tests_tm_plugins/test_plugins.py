import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Проверки Plugins")
class TestPlugins(BaseCase):

    def setup(self):

        self.snp_check_value_for_nsi = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check NSI","InitialTransitionId":"6ce8ec25-c09b-4bf1-81a9-541f749bac7c","ProcessContext":{"lpu":{"idLpu":"test_value"}},"roleContext":{}}'
        self.snp_check_value_for_nsi_array = '{"WorkflowId":"09872eef-6180-4f5f-9137-c33ce60ad416","Name":"Check NSI","InitialTransitionId":"6ce8ec25-c09b-4bf1-81a9-541f749bac7c","ProcessContext":{"arrayLpu":[{"id":"1","idLpu":"test_array_value","isDeleted":false}]},"roleContext":{}}'

        self.mts_check_value_for_nsi = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"lpu":{"idLpu":"test_value"}},"roleContext":{}}'
        self.mts_check_value_for_nsi_array = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"arrayLpu":[{"id":"1","idLpu":"test_array_value","isDeleted":false}]},"roleContext":{}}'

        self.mts_check_empty_for_nsi = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"lpu":{"idLpu":""}},"roleContext":{}}'
        self.mts_check_empty_for_nsi_array = '{"processId":"example","transitionId":"54cc8225-6f28-40c2-a2c3-1755200c7321","processContext":{"arrayLpu":[{"id":"1","idLpu":"","isDeleted":false}]},"roleContext":{}}'

        self.last_stage_id = 'a22cfdd7-6a54-4ed2-9b49-6d527afae3d1'

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
        Assertions.assert_json_value_by_name(mts_no_value_in_array, 'message','Object reference not set to an instance of an object.',
                                             'Получена неожиданная ошибка')

        #проверка что статус успешно меняется
        move = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                 data=self.mts_check_req)
        Assertions.assert_json_value_by_name(move, 'success', True, 'Смена статуса закончилась неудачей')
