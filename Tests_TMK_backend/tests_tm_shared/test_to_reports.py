import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure


@allure.epic("Полноценные проверки Shared")
class TestReports(BaseCase):
    def setup(self):

        self.report_template_id = "a819cbe4-41ee-462c-a2ac-f42c67bbe7d4" #id шаблона "QA report" у отчёта "QA-test"
        self.template_search = "{'resourceType':'Parameters','parameter':[{'name':'pageNumber','valuePositiveInt':1},{'name':'pageSize','valuePositiveInt':10},{'name':'descendingOrderByName','valueBoolean':true},{'name':'name','valueString':'QA report'},{'name':'reportId','valueString':'68b2ec93-6401-49da-8362-8d22e0ebfd2b'}]}"
        self.for_session_id = "{\"email\": \"reg_admin@test.com\",\"password\": \"123\"}"
        self.get_report_data = "{'resourceType':'Parameters','parameter':[{'name':'skip','valuePositiveInt':0},{'name':'take','valuePositiveInt':10},{'name':'descendingOrder','valueBoolean':true}]}"
        self.old_sessionId = "7f619751-5faa-403f-ba24-61b79afbf33e"

    @allure.feature("Негативные проверки на вызов TM.Reports")
    def test_negative_reports(self):

        #получение некорректного шаблона отчёта
        get_incorrect = MyRequests.get(f'/tm-shared/api/Reports/templates/{config.default_id}')
        error_message = get_incorrect.json()['Issue'][0]['Details']['Coding'][0]['DisplayElement']['Value']
        Assertions.assert_expectedvalue_equal_receivedvalue(get_incorrect, 'Не удалось найти заданный шаблон', error_message, 'Ожидаемая ошибка не получена')
        Assertions.assert_code_status(get_incorrect, 500)

        #поиск шаблонов с некорректным id отчёта
        self.template_search = self.template_search.replace('68b2ec93-6401-49da-8362-8d22e0ebfd2b', config.default_id)
        incorrect_template_search = MyRequests.post('/tm-shared/api/Reports/templates/search',headers={'Content-Type': 'application/json-patch+json'},
                                          data=self.template_search)
        template_value = incorrect_template_search.json()['entry']
        Assertions.assert_expectedvalue_equal_receivedvalue(incorrect_template_search, [], template_value, 'Информация должна отсутствовать')

        #запрос на получение отчёта по шаблону без sessionId
        get_report_data_no_sessionId = MyRequests.post(f'/tm-shared/api/Reports/getReportData/{self.report_template_id}',headers={'Content-Type': 'application/json-patch+json'},
                                          data=self.get_report_data)
        Assertions.assert_code_status(get_report_data_no_sessionId, 401)

        #запрос на получение отчёта по шаблону с протухшим sessionId
        get_report_data_old_sessionId = MyRequests.post(f'/tm-shared/api/Reports/getReportData/{self.report_template_id}',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{self.old_sessionId}'},
                                                       data=self.get_report_data)
        Assertions.assert_code_status(get_report_data_old_sessionId, 401)

        #запрос на получение отчёта с некорректным id шаблона
        request_to_login = MyRequests.post('/tm.doctorportal/api/auth/sign-in',headers={'Content-Type': 'application/json'}, data=self.for_session_id)
        session_id = request_to_login.json()['result']['sessionId']

        get_report_data_incorrect_templateId = MyRequests.post(f'/tm-shared/api/Reports/getReportData/{config.default_id}',
                                          headers={'Content-Type': 'application/json-patch+json','Authorization': f'{session_id}'},
                                          data=self.get_report_data)
        error_in_report = get_report_data_incorrect_templateId.json()['Issue'][0]['Details']['Coding'][0]['DisplayElement']['Value']
        Assertions.assert_expectedvalue_equal_receivedvalue(get_report_data_incorrect_templateId, f"Шаблон отчёта с идентификатором {config.default_id} не найден",
                                                            error_in_report,'Ожидаемый тип не получен')
        Assertions.assert_code_status(get_report_data_incorrect_templateId, 500)

    @allure.feature("Позитивные проверки на вызов TM.Reports")
    def test_correct_reports(self):

        #получение корректного шаблона отчёта
        get = MyRequests.get(f'/tm-shared/api/Reports/templates/{self.report_template_id}')
        value = get.json()['contentTypeElement']['value']
        Assertions.assert_expectedvalue_equal_receivedvalue(get, 'text/plain', value, 'Ожидаемый тип не получен')
        Assertions.assert_code_status(get, 200)

        #поиск шаблона выбранного отчёта
        template_search = MyRequests.post('/tm-shared/api/Reports/templates/search', headers={'Content-Type': 'application/json-patch+json'},
                                          data=self.template_search)
        template_value = template_search.json()['entry'][0]['fullUrlElement']['value']
        Assertions.assert_expectedvalue_equal_receivedvalue(template_search, f'Template/{self.report_template_id}', template_value, 'Полученный шаблон не равен ожидаемому')

        #получение session_id
        request_to_login = MyRequests.post('/tm.doctorportal/api/auth/sign-in', headers={'Content-Type': 'application/json'}, data=self.for_session_id)
        session_id = request_to_login.json()['result']['sessionId']

        #запрос на получение отчёта по шаблону
        get_report_data = MyRequests.post(f'/tm-shared/api/Reports/getReportData/{self.report_template_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{session_id}'},
                                          data=self.get_report_data)
        report_value = get_report_data.json()['contentTypeElement']['value']
        Assertions.assert_expectedvalue_equal_receivedvalue(get_report_data, 'text/plain', report_value, 'Ожидаемый тип не получен')
        Assertions.assert_code_status(get, 200)