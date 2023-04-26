import datetime
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Проверки Roles")
class TestCheckRole(BaseCase):

    def setup(self):

        self.create_correct = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'642852a4-9f55-4429-becb-cfc81e953584','ProcessContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}}}"
        self.create_another_role = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'642852a4-9f55-4429-becb-cfc81e953584','ProcessContext':{},'roleContext':{'68b19d33-0acc-4adc-a9a1-25874e5a6ab2':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}}}"
        self.create_another_data_in_validator = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'642852a4-9f55-4429-becb-cfc81e953584','ProcessContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682','SNILS':'48368377143'}}}"
        self.create_without_required_data = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'642852a4-9f55-4429-becb-cfc81e953584','ProcessContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e'}}}"
        self.create_no_role = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'642852a4-9f55-4429-becb-cfc81e953584','ProcessContext':{},'roleContext':{}}"
        self.create_without_role_validator = "{'WorkflowId':'75e7a4ea-10ef-4c63-bdfe-5041a437fa1c','Name':'Check role','InitialTransitionId':'60a7bbc4-c05a-498c-828e-8bdafcde8953','ProcessContext':{},'roleContext':{}}"

        self.move_another_role = "{'processId':'example','transitionId':'4d4ec301-3550-4fd0-8350-9c1c18f31f7a','processContext':{},'roleContext':{'68b19d33-0acc-4adc-a9a1-25874e5a6111':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}}}"
        self.move_another_data_in_validator = "{'processId':'example','transitionId':'4d4ec301-3550-4fd0-8350-9c1c18f31f7a','processContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'3b4b37cd-ef0f-4017-9eb4-2fe49142f682','SNILS':'48368377143'}}}"
        self.move_without_required_data = "{'processId':'example','transitionId':'4d4ec301-3550-4fd0-8350-9c1c18f31f7a','processContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e'}}}"
        self.move_no_role = "{'processId':'example','transitionId':'4d4ec301-3550-4fd0-8350-9c1c18f31f7a','processContext':{},'roleContext':{}}"
        self.move_without_role_validator = "{'processId':'example','transitionId':'d8989508-7b03-430f-a664-4f530bef400e','ProcessContext':{},'roleContext':{}}"
        self.move_correct = "{'processId':'example','transitionId':'4d4ec301-3550-4fd0-8350-9c1c18f31f7a','processContext':{},'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}}}"

    @allure.feature("Тесты на проверку роли при создании направления и смене статуса")
    def testCheckRole(self):

        #настроена на переходе проверка на передачу определенной роли и передать всё корректно
        create_correct = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_correct)
        Assertions.assert_json_value_by_name(create_correct, 'success', True, 'Создание направления завершилось с ошибкой')
        processId = create_correct.json()['processId']

        #передать другую роль и получить ошибку
        create_another_role = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_another_role)
        Assertions.assert_json_value_by_name(create_another_role, 'message', 'Invalid role context ', "Получен неожиданный результат в результате передачи неверной роли")

        #передать несуществующую роль
        self.create_another_role = self.create_another_role.replace('68b19d33-0acc-4adc-a9a1-25874e5a6ab2', '68b19d33-0acc-4adc-a9a1-25874e5a6111')
        create_not_exist_role = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_another_role)
        Assertions.assert_json_value_by_name(create_not_exist_role, 'message', 'Role context not found or is not a role schema', "Получен неожиданный результат в результате передачи несуществующей роли")

        #передать иное значение параметра от проверяемого в валидаторе
        create_another_data_in_validator = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_another_data_in_validator)
        Assertions.assert_json_value_by_name(create_another_data_in_validator, 'message', 'Invalid role context Ошибка при несоответствии данных роли',
                                             "Получен неожиданный результат в результате передачи неверного проверяемого значения роли")

        #не передать обязательный параметр у роли
        create_without_required_data = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_without_required_data)
        Assertions.assert_json_value_by_name(create_without_required_data, 'message', "PropertyRequired #/SNILS in schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             "Получен неожиданный результат в результате отсутствия обязательного параметра в роли")

        #не передать роль в ролевом контексте
        create_no_role = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_no_role)
        Assertions.assert_json_value_by_name(create_no_role, 'message', 'For transition 642852a4-9f55-4429-becb-cfc81e953584 Role context is required.',
                                             "Получен неожиданный результат в результате отсутствия роли")

        #на переходе нет проверки на роль и заявка создается без нее
        create_without_role_validator = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.create_without_role_validator)
        Assertions.assert_json_value_by_name(create_without_role_validator, 'success', True, 'Создание направления завершилось с ошибкой')
        processId_without_role_validator = create_without_role_validator.json()['processId']

        #провести то же самое только для moveToStage
        self.move_another_role = self.move_another_role.replace('example', processId)
        self.move_another_data_in_validator = self.move_another_data_in_validator.replace('example', processId)
        self.move_without_required_data = self.move_without_required_data.replace('example', processId)
        self.move_no_role = self.move_no_role.replace('example', processId)
        self.move_without_role_validator = self.move_without_role_validator.replace('example', processId_without_role_validator)
        self.move_correct = self.move_correct.replace('example', processId)

        #передать несуществующую роль
        move_not_exist_role = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.move_another_role)
        Assertions.assert_json_value_by_name(move_not_exist_role, 'message', 'Role context not found or is not a role schema', "Получен неожиданный результат в результате передачи несуществующей роли")

        #передать другую роль и получить ошибку
        self.move_another_role = self.move_another_role.replace('68b19d33-0acc-4adc-a9a1-25874e5a6111', '68b19d33-0acc-4adc-a9a1-25874e5a6ab2')
        move_another_role = MyRequests.post('/tm-core/api/Commands/MoveToStage', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                              data=self.move_another_role)
        Assertions.assert_json_value_by_name(move_another_role, 'message', 'Invalid role context ', "Получен неожиданный результат в результате передачи несуществующей роли")

        # передать иное значение параметра от проверяемого в валидаторе
        move_another_data_in_validator = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                           data=self.move_another_data_in_validator)
        Assertions.assert_json_value_by_name(move_another_data_in_validator, 'message','Invalid role context Ошибка при несоответствии данных роли',
                                             "Получен неожиданный результат в результате передачи неверного проверяемого значения роли")

        # не передать обязательный параметр у роли
        move_without_required_data = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                       data=self.move_without_required_data)
        Assertions.assert_json_value_by_name(move_without_required_data, 'message',"Invalid role schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             "Получен неожиданный результат в результате отсутствия обязательного параметра в роли")

        # не передать роль в ролевом контексте
        move_no_role = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                         data=self.move_no_role)
        Assertions.assert_json_value_by_name(move_no_role, 'message','For transition 4d4ec301-3550-4fd0-8350-9c1c18f31f7a Role context is required.',
                                             "Получен неожиданный результат в результате отсутствия роли")

        # на переходе нет проверки на роль и статус меняется без нее
        move_without_role_validator = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                        data=self.move_without_role_validator)
        Assertions.assert_json_value_by_name(move_without_role_validator, 'success', True,'Смена статуса направления завершилась с ошибкой')

        #передать всё корректно при смене статуса
        move_correct = MyRequests.post('/tm-core/api/Commands/MoveToStage',headers={'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                                        data=self.move_correct)
        Assertions.assert_json_value_by_name(move_correct, 'success', True,'Смена статуса направления завершилась с ошибкой')

# проверка что метод GetTransitionAvailableProcesses отвечает успешно по существующей роли
@allure.epic("Проверки Roles")
class TestCheckGetTransitionAvailableProcessesWithRole(BaseCase):

    def setup(self):

        self.search = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}},'skip':0,'take':1}"
        self.no_snils = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e'}},'skip':0,'take':1}"
        self.no_context = "{'skip':0,'take':1}"

    @allure.feature("Тесты на проверку GetTransitionAvailableProcesses")
    def testCheckRole(self):

        #передать всё корректно
        correct = MyRequests.post('/tm-core/api/Queries/GetTransitionAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(correct, 'success', True, 'Запрос завершился ошибкой')

        #передать несуществующую роль
        self.search = self.search.replace('8c293df2-ea96-42cd-9c1a-1e4e21df4497', config.default_id)
        not_exist_role = MyRequests.post('/tm-core/api/Queries/GetTransitionAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(not_exist_role, 'message', 'Role context not found or is not a role schema', 'Запрос не завершился ошибкой')

        #не передать обязательный параметр у роли
        no_snils = MyRequests.post('/tm-core/api/Queries/GetTransitionAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_snils)
        Assertions.assert_json_value_by_name(no_snils, 'message', "PropertyRequired #/SNILS in schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             'Запрос не завершился ошибкой')

        #не передать ролевой контекст
        no_context = MyRequests.post('/tm-core/api/Queries/GetTransitionAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_context)
        Assertions.assert_json_value_by_name(no_context, 'success', True, 'Запрос завершился ошибкой')

# то же самое по GetReadAvailableProcesses
@allure.epic("Проверки Roles")
class TestCheckGetReadAvailableProcessesWithRole(BaseCase):

    def setup(self):

        self.search = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}},'skip':0,'take':1}"
        self.no_snils = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e'}},'skip':0,'take':1}"
        self.no_context = "{'skip':0,'take':1}"

    @allure.feature("Тесты на проверку GetReadAvailableProcesses")
    def testCheckRole(self):

        #передать всё корректно
        correct = MyRequests.post('/tm-core/api/Queries/GetReadAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(correct, 'success', True, 'Запрос завершился ошибкой')

        #передать несуществующую роль
        self.search = self.search.replace('8c293df2-ea96-42cd-9c1a-1e4e21df4497', config.default_id)
        not_exist_role = MyRequests.post('/tm-core/api/Queries/GetReadAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(not_exist_role, 'message', 'Role context not found or is not a role schema', 'Запрос не завершился ошибкой')

        #не передать обязательный параметр у роли
        no_snils = MyRequests.post('/tm-core/api/Queries/GetReadAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_snils)
        Assertions.assert_json_value_by_name(no_snils, 'message', "PropertyRequired #/SNILS in schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             'Запрос не завершился ошибкой')

        #не передать ролевой контекст
        no_context = MyRequests.post('/tm-core/api/Queries/GetReadAvailableProcesses', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_context)
        Assertions.assert_json_value_by_name(no_context, 'success', True, 'Запрос завершился ошибкой')

# то же самое по GetAvailableTransitions
@allure.epic("Проверки Roles")
class TestCheckGetAvailableTransitionsWithRole(BaseCase):

    def setup(self):

        self.search = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'}},'skip':0,'take':1}"
        self.no_snils = "{'roleContext':{'8c293df2-ea96-42cd-9c1a-1e4e21df4497':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e'}},'skip':0,'take':1}"
        self.no_context = "{'skip':0,'take':1}"

    @allure.feature("Тесты на проверку GetAvailableTransitions")
    def testCheckRole(self):

        #передать всё корректно
        correct = MyRequests.post('/tm-core/api/Queries/GetAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(correct, 'success', True, 'Запрос завершился ошибкой')

        #передать несуществующую роль
        self.search = self.search.replace('8c293df2-ea96-42cd-9c1a-1e4e21df4497', config.default_id)
        not_exist_role = MyRequests.post('/tm-core/api/Queries/GetAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(not_exist_role, 'message', 'Role context not found or is not a role schema', 'Запрос не завершился ошибкой')

        #не передать обязательный параметр у роли
        no_snils = MyRequests.post('/tm-core/api/Queries/GetAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_snils)
        Assertions.assert_json_value_by_name(no_snils, 'message', "PropertyRequired #/SNILS in schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             'Запрос не завершился ошибкой')

        #не передать ролевой контекст
        no_context = MyRequests.post('/tm-core/api/Queries/GetAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_context)
        Assertions.assert_json_value_by_name(no_context, 'success', True, 'Запрос завершился ошибкой')

# GetProcessWithAvailableTransitions
@allure.epic("Проверки Roles")
class TestCheckGetProcessWithAvailableTransitionsWithRole(BaseCase):

    def setup(self):

        self.search = '{"ProcessId":"ccb75e26-a418-41cc-8bed-030f4a286b21","roleContext":{"8c293df2-ea96-42cd-9c1a-1e4e21df4497":{"organization":"6c34dc18-cab0-4e53-aba8-cea197f0ab5e","SNILS":"48368377143"}}}'
        self.no_context = '{"ProcessId":"ccb75e26-a418-41cc-8bed-030f4a286b21"}'

    @allure.feature("Тесты на проверку GetProcessWithAvailableTransitions")
    def testCheckRole(self):

        #передать всё корректно
        correct = MyRequests.post('/tm-core/api/Queries/GetProcessWithAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(correct, 'success', True, 'Запрос завершился ошибкой')

        #передать несуществующую роль
        self.search = self.search.replace('8c293df2-ea96-42cd-9c1a-1e4e21df4497', config.default_id)
        not_exist_role = MyRequests.post('/tm-core/api/Queries/GetProcessWithAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(not_exist_role, 'message', 'Role context not found or is not a role schema', 'Запрос не завершился ошибкой')

        #передать роль, не относящуюся к заявке
        self.search = self.search.replace(config.default_id, '68b19d33-0acc-4adc-a9a1-25874e5a6ab2')
        incorrect_role = MyRequests.post('/tm-core/api/Queries/GetProcessWithAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        array_at = incorrect_role.json()['result']['availableTransitions']
        if array_at != []:
            for i in range(len(array_at)):
                Assertions.assert_value_equeals_expected(array_at[i]['roleSchemaIds'], [])
        else:
            Assertions.assert_expectedvalue_equal_receivedvalue(incorrect_role, [], array_at, 'Список доступных переходов не пуст')

        #не передать ролевой контекст
        no_context = MyRequests.post('/tm-core/api/Queries/GetProcessWithAvailableTransitions', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_context)
        array_at_no_context = incorrect_role.json()['result']['availableTransitions']
        if array_at_no_context != []:
            for i in range(len(array_at_no_context)):
                Assertions.assert_value_equeals_expected(array_at_no_context[i]['roleSchemaIds'], [])
        else:
            Assertions.assert_expectedvalue_equal_receivedvalue(no_context, [], array_at_no_context, 'Список доступных переходов не пуст')

# GetProcessHistory
@allure.epic("Проверки Roles")
class TestCheckGetProcessHistoryWithRole(BaseCase):

    def setup(self):

        self.search = '{"ProcessId":"ccb75e26-a418-41cc-8bed-030f4a286b21","roleContext":{"8c293df2-ea96-42cd-9c1a-1e4e21df4497":{"organization":"6c34dc18-cab0-4e53-aba8-cea197f0ab5e","SNILS":"48368377143"}}}'
        self.no_snils = '{"ProcessId":"ccb75e26-a418-41cc-8bed-030f4a286b21","roleContext":{"8c293df2-ea96-42cd-9c1a-1e4e21df4497":{"organization":"6c34dc18-cab0-4e53-aba8-cea197f0ab5e"}}}'
        self.no_context = '{"ProcessId":"ccb75e26-a418-41cc-8bed-030f4a286b21"}'

    @allure.feature("Тесты на проверку GetProcessHistory")
    def testCheckRole(self):

        #передать всё корректно
        correct = MyRequests.post('/tm-core/api/Queries/GetProcessHistory', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(correct, 'success', True, 'Запрос завершился ошибкой')

        #передать несуществующую роль
        self.search = self.search.replace('8c293df2-ea96-42cd-9c1a-1e4e21df4497', config.default_id)
        not_exist_role = MyRequests.post('/tm-core/api/Queries/GetProcessHistory', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(not_exist_role, 'message', 'Role context not found or is not a role schema', 'Запрос не завершился ошибкой')

        #передать роль, не относящуюся к заявке
        self.search = self.search.replace(config.default_id, '68b19d33-0acc-4adc-a9a1-25874e5a6ab2')
        incorrect_role = MyRequests.post('/tm-core/api/Queries/GetProcessHistory', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.search)
        Assertions.assert_json_value_by_name(incorrect_role, 'success', True, 'Запрос завершился ошибкой')

        #не передать обязательный параметр у роли
        no_snils = MyRequests.post('/tm-core/api/Queries/GetProcessHistory', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_snils)
        Assertions.assert_json_value_by_name(no_snils, 'message', "Invalid role schema {\n  \"type\": \"object\",\n  \"$schema\": \"http://json-schema.org/draft-04/schema#\",\n  \"required\": [\n    \"SNILS\"\n  ],\n  \"properties\": {\n    \"SNILS\": {\n      \"type\": \"string\"\n    },\n    \"organization\": {\n      \"type\": \"string\"\n    }\n  }\n}",
                                             'Запрос не завершился ошибкой')

        #не передать ролевой контекст
        no_context = MyRequests.post('/tm-core/api/Queries/GetProcessHistory', headers = {'Authorization': f'{config.token_tm_core}','Content-Type': 'application/json-patch+json'},
                                  data=self.no_context)
        Assertions.assert_json_value_by_name(no_context, 'success', True, 'Запрос завершился ошибкой')



