import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Проверки обращений к НСИ из Reports")
class TestNSIandVersion(BaseCase):

    @allure.feature("Обращения к НСИ")
    def test_nsi(self):

        #получение списка всех справочников НСИ
        req_dict = MyRequests.get('/tm_reports/api/nsi/dictionaries')
        Assertions.assert_code_status(req_dict, 200)

        #получение списка названий всех справочников НСИ
        req_dict_names = MyRequests.get('/tm_reports/api/nsi/dictionaries/names')
        Assertions.assert_code_status(req_dict_names, 200)

    @allure.feature("Получение версии")
    def test_version(self):

        get_version = MyRequests.get('/tm_reports/api/_version')
        Assertions.assert_code_status(get_version, 200)

@allure.epic("Полноценные проверки Report") #добавить текст на получение данных отчёта с expression и roleContext
class TestReport(BaseCase):
    def setup(self):

        self.report_title = "rep_2xghfdbc1kadcw5voveiwg"
        self.templateId_application = "30d8d2df-336e-4cc7-93b1-bbad875bf7a6"
        self.templateId_aggregate = "f9f4e1bc-54d5-4017-91e1-b247079c0315"
        self.report_columns = ["process_id","human_friendly_id","update_time","current_stage_id","status_name","business_status_code","workflow_id","create_time","col_xkrnp0loeowy9y0te3p4q"]
        self.report_columns_aggregate = ["Код статуса по справочнику НСИ","Количество"]

        self.noname = "{\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"
        self.nolink = "{\"name\": \"Autocheck\",\"type\": \"QA-area\"}"
        self.notype = "{\"link\": \"bfe35b34-2824-4af6-95c9-49965998f081\", \"name\": \"Autocheck\"}"
        self.dublicate = "{\"name\":\"QA-test\",\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"
        self.wrong_data = "{\"name\":\"test\",\"link\":\"50752145-1d1b-42cc-b052-2892a84485ed\",\"type\":\"test\"}"

        self.create = "{\"name\":\"autotest\",\"link\":\"bfe35b34-2824-4af6-95c9-49965998f081\",\"type\":\"QA-area\"}"

        self.get_reports_few = "{\"pageNumber\":1,\"pageSize\":10,\"reportName\":\"QA-test\"}"
        self.no_ColumnTitle = "{\"skip\":0,\"take\":20,\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"sign\":\"Equals\",\"values\":[\"17\"],\"valueType\":\"text\"}]}"
        self.no_Sign = "{\"skip\":0,\"take\":20,\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"columnTitle\":\"business_status_code\",\"values\":[\"17\"],\"valueType\":\"text\"}]}"
        self.no_Values = "{\"skip\":0,\"take\":20,\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"Equals\",\"valueType\":\"text\"}]}"
        self.no_ValueType = "{\"skip\":0,\"take\":20,\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"Equals\",\"values\":[\"17\"]}]}"

        self.no_agg_groupByColumnTitle =  "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')
        self.no_agg_description = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}"
        self.no_agg_AggregationFunction = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')
        self.no_agg_ColumnTitle = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')
        self.no_agg_Sign = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')
        self.no_agg_Values = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"valueType\":\"text\"}]}".encode('UTF-8')
        self.no_agg_ValueType = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"]}]}".encode('UTF-8')
        self.byTemplate = "{\"RoleContext\":\"{\n  \"roleContext\": [\n    {\n      \"portalUser\": {\n        \"minRoleRank\": \"example\",\n        \"organizationId\": \"6c34dc18-cab0-4e53-aba8-cea197f0ab5e\"\n      }\n    }\n  ]\n}\",\"skip\":0,\"take\":20,\"orderingField\":\"process_id\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"status_name\",\"business_status_code\",\"col_xkrnp0loeowy9y0te3p4q\",\"col_9y51rbfhl0agdf0w4rh57w\"]}"

        self.get_reports = "{\"pageNumber\":1,\"pageSize\":20,\"reportName\":\"QA-test\"}"
        self.get_report_data = "{\"skip\":0,\"take\":20,\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"Equals\",\"values\":[\"17\"],\"valueType\":\"text\"}]}"
        self.get_aggregate_report_data = "{\"skip\":0,\"take\":20,\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')

        self.get_report_to_excel = "{\"orderingField\":\"update_time\",\"descendingOrder\":true,\"reportColumns\":[\"process_id\",\"human_friendly_id\",\"update_time\",\"current_stage_id\",\"status_name\",\"business_status_code\",\"workflow_id\",\"create_time\",\"col_xkrnp0loeowy9y0te3p4q\"],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"Equals\",\"values\":[\"17\"],\"valueType\":\"text\"}]}"
        self.get_aggregate_report_to_excel = "{\"descendingOrder\":true,\"groupByColumnTitle\":\"business_status_code\",\"reportColumns\":[{\"id\":\"cfbef883-4cc7-4cdb-8a14-60821eb0a2e0\",\"filters\":[],\"description\":\"Количество\",\"aggregationFunction\":\"Count\"}],\"filters\":[{\"columnTitle\":\"business_status_code\",\"sign\":\"NotEquals\",\"values\":[\"2\"],\"valueType\":\"text\"}]}".encode('UTF-8')

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
        Assertions.assert_json_value_by_name(create, 'name', 'autotest', 'Создание отчета завершилось неуспешно')

        reportId = create.json()['id']

        get = MyRequests.get(f'/tm_reports/api/Report/{reportId}')
        Assertions.assert_json_value_by_name(get, 'name', 'autotest', 'Получение отчета завершилось неуспешно')

        self.create = self.create.replace('autotest', 'autotest update')

        update = MyRequests.put(f'/tm_reports/api/Report/{reportId}', headers={'Content-Type': 'application/json'}, data=self.create)
        Assertions.assert_json_value_by_name(update, 'name', "autotest update", 'Обновление отчета завершилось неуспешно')

        delete = MyRequests.delete(f'/tm_reports/api/Report/{reportId}')
        Assertions.assert_body(delete, f'Отчет {reportId} удален.')

    @allure.feature("Проверка негативных запросов к методам получения отчётов, построения файлов")
    def test_negative_get_reports_data(self):

        #обращение к методу GetReports с малым pageSize
        # get_reports = MyRequests.post('/tm_reports/api/Report/GetReports', headers={'Content-Type': 'application/json'},data=self.get_reports_few)
        # Assertions.assert_json_value_by_name(get_reports, 'Message', 'Количество элементов на странице не может быть меньше 20 и больше 100 ',
        #                                                     'В ответе не найден ожидаемый отчёт')
        #
        # #обращение к GetReportData с несуществующим reportTitle
        # get_report_data = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{config.default_id}',headers={'Content-Type': 'application/json'},
        #                                   data=self.get_report_data)
        # Assertions.assert_json_value_by_name(get_report_data, 'Message', f"Отчет c названием '{config.default_id}' не найден.",
        #                                      "Ожидаемая ошибка о неверном reportTitle не получена")
        #
        # # обращение к GetReportData без columnTitle, Sign, Values, ValueType
        # get_report_data_no_ColumnTitle = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                   data=self.no_ColumnTitle)
        # Assertions.assert_json_value_by_name(get_report_data_no_ColumnTitle, 'Message', "Если Filters задан, то ColumnTitle - обязательный параметр.",
        #                                      "Ожидаемая ошибка об отсутствии ColumnTitle не получена")
        #
        # get_report_data_no_Sign = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                   data=self.no_Sign)
        # Assertions.assert_json_value_by_name(get_report_data_no_Sign, 'Message', "Если Filters задан, то Sign - обязательный параметр и не может быть значением по умолчанию (Default).",
        #                                      "Ожидаемая ошибка об отсутствии Sign не получена")
        #
        # get_report_data_no_Values = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                   data=self.no_Values)
        # Assertions.assert_json_value_by_name(get_report_data_no_Values, 'Message', "Если Filters задан, и нет проверки на заполненность поля, то Values - обязательный параметр.",
        #                                      "Ожидаемая ошибка об отсутствии Values не получена")
        #
        # get_report_data_no_ValueType = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                   data=self.no_ValueType)
        # Assertions.assert_json_value_by_name(get_report_data_no_ValueType, 'Message', "Если Filters задан, то ValueType - обязательный параметр и не может быть значением по умолчанию (Default).",
        #                                      "Ожидаемая ошибка об отсутствии ValueType не получена")
        #
        # #обращение к ExportReportToExcel с несуществующим reportTitle
        # export_report_to_excel = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={config.default_id}&count=100',
        #                                          headers={'Content-Type': 'application/json'},data=self.get_report_to_excel)
        # Assertions.assert_json_value_by_name(export_report_to_excel, 'Message', f"Отчет c названием '{config.default_id}' не найден.",
        #                                      "Ожидаемая ошибка о неверном reportTitle не получена")
        #
        # # обращение к ExportReportToExcel без columnTitle, Sign, Values, ValueType
        # export_report_to_excel_no_ColumnTitle = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={self.report_title}&count=100'
        #                                                         ,headers={'Content-Type': 'application/json'},data=self.no_ColumnTitle)
        # Assertions.assert_json_value_by_name(export_report_to_excel_no_ColumnTitle, 'Message', "Если Filters задан, то ColumnTitle - обязательный параметр.",
        #                                      "Ожидаемая ошибка об отсутствии ColumnTitle не получена")
        #
        # export_report_to_excel_no_Sign = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={self.report_title}&count=100',
        #                                                  headers={'Content-Type': 'application/json'},data=self.no_Sign)
        # Assertions.assert_json_value_by_name(export_report_to_excel_no_Sign, 'Message', "Если Filters задан, то Sign - обязательный параметр и не может быть значением по умолчанию (Default).",
        #                                      "Ожидаемая ошибка об отсутствии Sign не получена")
        #
        # export_report_to_excel_no_Values = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={self.report_title}&count=100',
        #                                                    headers={'Content-Type': 'application/json'},data=self.no_Values)
        # Assertions.assert_json_value_by_name(export_report_to_excel_no_Values, 'Message', "Если Filters задан, и нет проверки на заполненность поля, то Values - обязательный параметр.",
        #                                      "Ожидаемая ошибка об отсутствии Values не получена")
        #
        # export_report_to_excel_no_ValueType = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={self.report_title}&count=100',
        #                                                       headers={'Content-Type': 'application/json'},data=self.no_ValueType)
        # Assertions.assert_json_value_by_name(export_report_to_excel_no_ValueType, 'Message', "ValueType не может быть значением по умолчанию.",
        #                                      "Ожидаемая ошибка об отсутствии ValueType не получена")
        #
        # #обращение к GetAggregateReportData с несуществующим reportTitle
        # get_aggregate_report_data = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{config.default_id}',headers={'Content-Type': 'application/json'},
        #                                             data=self.get_aggregate_report_data)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data, 'Message',f"Отчет c названием '{config.default_id}' не найден.",
        #                                      "Ожидаемая ошибка о неверном reportTitle не получена")
        #
        # #обращение к GetAggregateReportData без groupByColumnTitle
        # get_aggregate_report_data_no_groupByColumnTitle = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_groupByColumnTitle)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_groupByColumnTitle, 'Message','GroupByColumnTitle - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии groupByColumnTitle не получена")
        #
        # # обращение к GetAggregateReportData без description
        # get_aggregate_report_data_no_description = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_description)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_description, 'Message','Если ReportColumns задан, то Description - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии description не получена")
        #
        # # обращение к GetAggregateReportData без AggregationFunction
        # get_aggregate_report_data_no_AggregationFunction = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_AggregationFunction)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_AggregationFunction, 'Message','Если ReportColumns задан, то AggregationFunction - обязательный параметр и не может быть значением по умолчанию (Default).',
        #                                      "Ожидаемая ошибка об отсутствии AggregationFunction не получена")
        #
        # # обращение к GetAggregateReportData без ColumnTitle
        # get_aggregate_report_data_no_ColumnTitle = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_ColumnTitle)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_ColumnTitle, 'Message','Если Filters задан, то ColumnTitle - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии ColumnTitle не получена")
        #
        # # обращение к GetAggregateReportData без Sign
        # get_aggregate_report_data_no_Sign = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_Sign)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_Sign, 'Message','Если Filters задан, то Sign - обязательный параметр и не может быть значением по умолчанию (Default).',
        #                                      "Ожидаемая ошибка об отсутствии Sign не получена")
        #
        # # обращение к GetAggregateReportData без Values
        # get_aggregate_report_data_no_Values = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_Values)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_Values, 'Message','Если Filters задан, и нет проверки на заполненность поля, то Values - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии Values не получена")
        #
        # # обращение к GetAggregateReportData без ValueType
        # get_aggregate_report_data_no_ValueType = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_ValueType)
        # Assertions.assert_json_value_by_name(get_aggregate_report_data_no_ValueType, 'Message','Если Filters задан, то ValueType - обязательный параметр и не может быть значением по умолчанию (Default).',
        #                                      "Ожидаемая ошибка об отсутствии ValueType не получена")
        #
        # #обращение к ExportAggregateReportToExcel с несуществующим reportTitle
        # export_aggregate_report_data = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={config.default_id}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.get_aggregate_report_data)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data, 'Message',f"Отчет c названием '{config.default_id}' не найден.",
        #                                      "Ожидаемая ошибка о неверном reportTitle не получена")
        #
        # #обращение к ExportAggregateReportToExcel без groupByColumnTitle
        # export_aggregate_report_data_no_groupByColumnTitle = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_groupByColumnTitle)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_groupByColumnTitle, 'Message','GroupByColumnTitle - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии groupByColumnTitle не получена")
        #
        # # обращение к ExportAggregateReportToExcel без description
        # export_aggregate_report_data_no_description = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_description)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_description, 'Message','Если ReportColumns задан, то Description - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии description не получена")
        #
        # # обращение к ExportAggregateReportToExcel без AggregationFunction
        # export_aggregate_report_data_no_AggregationFunction = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_AggregationFunction)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_AggregationFunction, 'Message','Если ReportColumns задан, то AggregationFunction - обязательный параметр и не может быть значением по умолчанию (Default).',
        #                                      "Ожидаемая ошибка об отсутствии AggregationFunction не получена")
        #
        # # обращение к ExportAggregateReportToExcel без ColumnTitle
        # export_aggregate_report_data_no_ColumnTitle = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_ColumnTitle)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_ColumnTitle, 'Message','Если Filters задан, то ColumnTitle - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии ColumnTitle не получена")
        #
        # # обращение к ExportAggregateReportToExcel без Sign
        # export_aggregate_report_data_no_Sign = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_Sign)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_Sign, 'Message','Если Filters задан, то Sign - обязательный параметр и не может быть значением по умолчанию (Default).',
        #                                      "Ожидаемая ошибка об отсутствии Sign не получена")
        #
        # # обращение к ExportAggregateReportToExcel без Values
        # export_aggregate_report_data_no_Values = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_Values)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_Values, 'Message','Если Filters задан, и нет проверки на заполненность поля, то Values - обязательный параметр.',
        #                                      "Ожидаемая ошибка об отсутствии Values не получена")
        #
        # # обращение к ExportAggregateReportToExcel без ValueType
        # export_aggregate_report_data_no_ValueType = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count=100',headers={'Content-Type': 'application/json'},
        #                                             data=self.no_agg_ValueType)
        # Assertions.assert_json_value_by_name(export_aggregate_report_data_no_ValueType, 'Message','ValueType не может быть значением по умолчанию.',
        #                                      "Ожидаемая ошибка об отсутствии ValueType не получена")

        # обращение к методу tm_reports/api/Report/getReportData/bytemplate с некорректным ролевым контекстом по шаблону по заявкам
        self.byTemplate = self.byTemplate.replace('example', '3')
        byTemplate_application = MyRequests.post(f'/tm_reports/api/Report/getReportData/bytemplate/{self.templateId_application}',headers={'Content-Type': 'application/json'},
                                                 data=self.byTemplate)
        Assertions.assert_json_value_by_name(byTemplate_application, 'sum', None, 'Значение параметра sum не равно нулю')
        Assertions.assert_json_value_by_name(byTemplate_application, 'count', 0, 'Значение параметра count не равно нулю')

        # обращение к методу tm_reports/api/Report/getReportData/bytemplate с некорректным ролевым контекстом по агрегированному шаблону
        byTemplate_aggregate = MyRequests.post(f'/tm_reports/api/Report/getReportData/bytemplate/{self.templateId_aggregate}',headers={'Content-Type': 'application/json'},
                                                 data=self.byTemplate)
        assert byTemplate_aggregate.json()['sum']['Сумма (Количество)'] is None, 'Значение параметра Сумма (Количество) не равно нулю'
        Assertions.assert_json_value_by_name(byTemplate_aggregate, 'count', 0, 'Значение параметра count не равно нулю')

    @allure.feature("Проверка методов получения отчётов, построения файлов")
    def test_get_reports_data(self):

        #проверка метода GetReports
        get_reports = MyRequests.post('/tm_reports/api/Report/GetReports', headers={'Content-Type': 'application/json'}, data=self.get_reports)
        Assertions.assert_expectedvalue_equal_receivedvalue(get_reports, '68b2ec93-6401-49da-8362-8d22e0ebfd2b',
                                                            get_reports.json()['reports'][0]['id'], 'В ответе не найден ожидаемый отчёт')

        #проверка метода GetReportData
        get_report_data = MyRequests.post(f'/tm_reports/api/Report/GetReportData/{self.report_title}', headers={'Content-Type': 'application/json'},
                                          data=self.get_report_data)
        Assertions.assert_code_status(get_report_data, 200)

        #проверка что в записи отчёта отображаются все столбцы, что были переданы в запросе к GetReportData и
        #что в отчёте отображаются записи согласно фильтру business_status_code = 17
        report_array = get_report_data.json()['table']
        s = 0
        for i in range(len(report_array)):
            for j in range(len(self.report_columns)):
                if self.report_columns[j] in report_array[i]:
                    s += 1
            Assertions.assert_value_equeals_expected(len(self.report_columns), s)
            Assertions.assert_value_equeals_expected(report_array[i]['business_status_code'], '17')
            s = 0

        #проверка что в count ответа отображается верное число
        assert get_report_data.json()['count'] == len(report_array), 'Количество записей в отчёте неверно подсчитано'

        #проверка метода ExportReportToExcel
        export_report_to_excel = MyRequests.post(f'/tm_reports/api/Report/ExportReportToExcel?reportTitle={self.report_title}&count={len(report_array)}',
                                                 headers={'Content-Type': 'application/json'},data=self.get_report_to_excel)
        #в хедерах есть attachment, не понимаю как проверить xslx файл
        Assertions.assert_code_status(export_report_to_excel, 200)
        Assertions.assert_expectedvalue_equal_receivedvalue(export_report_to_excel, export_report_to_excel.headers['content-type'],
                                             "application/octet-stream", "Получен неожиданный header")

    @allure.feature("Проверка методов получения аггрегированных отчётов, построения файлов")
    def test_get_aggreaget_reports_data(self):

        #проверка метода GetAggregateReportData
        get_aggregate_report_data = MyRequests.post(f'/tm_reports/api/Report/GetAggregateReportData/{self.report_title}', headers={'Content-Type': 'application/json'},
                                          data=self.get_aggregate_report_data)
        Assertions.assert_code_status(get_aggregate_report_data, 200)

        #проверка что в записи отчёта отображаются все столбцы, что были переданы в запросе к GetAggregateReportData и
        #что в отчёте отображаются записи согласно фильтру business_status_code != 2
        report_aggregate_array = get_aggregate_report_data.json()['table']
        s = 0
        amount = 0
        for i in range(len(report_aggregate_array)):
            for j in range(len(self.report_columns_aggregate)):
                if self.report_columns_aggregate[j] in report_aggregate_array[i]:
                    s += 1
            amount += report_aggregate_array[i]['Количество']
            Assertions.assert_value_equeals_expected(len(self.report_columns_aggregate), s)
            assert report_aggregate_array[i]['Код статуса по справочнику НСИ'] != '2', "Фильтр на 'Код статуса по справочнику НСИ' не отработал"
            s = 0

        #проверка что в 'Сумма (Количество)' отчёта верно подсчитано значение
        Assertions.assert_expectedvalue_equal_receivedvalue(get_aggregate_report_data, amount,
                                                            get_aggregate_report_data.json()['sum']['Сумма (Количество)'], 'Значения количества не сходятся')

        #проверка что в count ответа отображается верное число
        assert get_aggregate_report_data.json()['count'] == len(report_aggregate_array), 'Количество записей в отчёте неверно подсчитано'

        #проверка метода ExportReportToExcel
        export_aggregate_report_to_excel = MyRequests.post(f'/tm_reports/api/Report/ExportAggregateReportToExcel?reportTitle={self.report_title}&count={len(report_aggregate_array)}',
                                                 headers={'Content-Type': 'application/json'},data=self.get_aggregate_report_to_excel)
        #в хедерах есть attachment, не понимаю как проверить xslx файл
        Assertions.assert_code_status(export_aggregate_report_to_excel, 200)
        Assertions.assert_expectedvalue_equal_receivedvalue(export_aggregate_report_to_excel, export_aggregate_report_to_excel.headers['content-type'],
                                             "application/octet-stream", "Получен неожиданный header")

@allure.epic("Полноценные проверки ReportColumn")
class TestReportColumn(BaseCase):

    def setup(self):

        self.report_id = "3bd98022-68da-400e-b780-cd403a72cda7"
        self.report_column_id = "e34ea885-dff0-4b9c-a6ff-3ed05bab15b9"
        self.report_column_id_second = "dcc9ab73-f9b8-4fdf-8b1b-b274158e227c"

        self.noreportId = "{\"name\":\"name\",\"jsonPathFromProcessContext\":\"$.lpu.address\",\"type\":1}"
        self.incorrectId = "{\"reportId\":\"3fa85f64-5717-4562-b3fc-2c963f66afa6\",\"jsonPathFromProcessContext\":\"$.lpu.address\",\"name\":\"name\",\"type\":\"text\"}"
        self.noname = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"jsonPathFromProcessContext\":\"$.lpu.address\",\"type\":\"text\"}"
        self.nojsonpath = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"name\":\"name\",\"type\":\"text\"}"
        self.notype = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"jsonPathFromProcessContext\":\"$.lpu.address\",\"name\":\"name\"}"
        self.create_dublicate_name = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"name\":\"Column Test\",\"jsonPathFromProcessContext\":\"$.lpu.address.third\",\"type\":\"text\"}"
        self.create_dublicate_jsonpath = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"name\":\"Column Test New\",\"jsonPathFromProcessContext\":\"$.lpu.address.second\",\"type\":\"text\"}"

        self.update = "{\"name\":\"Column Autotest Update\",\"jsonPathFromProcessContext\":\"$.lpu.update\"}"
        self.update_noname = "{\"jsonPathFromProcessContext\":\"$.lpu.address\"}"
        self.update_nojsonpath = "{\"name\":\"Column Test\"}"
        self.update_dublicate_jsonpath = "{\"name\":\"Column Test\",\"jsonPathFromProcessContext\":\"$.lpu.address.second\"}"
        self.update_dublicate_name = "{\"name\":\"Column Test\",\"jsonPathFromProcessContext\":\"$.lpu.address.third\"}"

        self.create = "{\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\",\"name\":\"Column Autotest\",\"jsonPathFromProcessContext\":\"$.lpu\",\"type\":\"text\"}"

    @allure.feature("Негативные тесты на колонку")
    def test_negative_reportcolumn(self):

        #создание колонки без reportId
        create_noreportId = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.noreportId)
        Assertions.assert_json_value_by_name(create_noreportId, 'Message', 'ReportId - обязательный параметр.', create_noreportId.json()['Message'])

        #создание колонки с некорректным reportId
        create_incorrectId = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.incorrectId)
        Assertions.assert_json_value_by_name(create_incorrectId, 'Message', f"Отчет с id = '{config.default_id}' не найден.",
                                             'Создание колонки с неверным ID успешно осуществилось')

        #создание колонки без name
        create_noname = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.noname)
        Assertions.assert_json_value_by_name(create_noname, 'Message', 'Name - обязательный параметр.', create_noname.json()['Message'])

        #создание колонки без JsonPathFromProcessContext
        create_nojsonpath = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.nojsonpath)
        Assertions.assert_json_value_by_name(create_nojsonpath, 'Message', 'JsonPathFromProcessContext - обязательный параметр.',
                                             create_nojsonpath.json()['Message'])

        #создание колонки без type
        create_type = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.notype)
        Assertions.assert_json_value_by_name(create_type, 'Message', 'Type - обязательный параметр и не может быть Default.',
                                             create_type.json()['Message'])

        #создать колонку с дублем name
        create_dublicate_name = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.create_dublicate_name)
        Assertions.assert_json_value_by_name(create_dublicate_name, 'Message', f"Колонка с именем 'Column Test' или json_path '$.lpu.address.third' для отчета '{self.report_id}' уже существует.",
                                             create_dublicate_name.json()['Message'])

        #создать колонку с дублем jsonpath
        create_dublicate_jsonpath = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.create_dublicate_jsonpath)
        Assertions.assert_json_value_by_name(create_dublicate_jsonpath, 'Message', f"Колонка с именем 'Column Test New' или json_path '$.lpu.address.second' для отчета '{self.report_id}' уже существует.",
                                             create_dublicate_jsonpath.json()['Message'])

        #обновить колонку с некорректным id
        update_incorrectId = MyRequests.put(f'/tm_reports/api/ReportColumn/{config.default_id}', headers={'Content-Type': 'application/json'},
                                             data=self.update)
        Assertions.assert_json_value_by_name(update_incorrectId, 'Message', f"Колонка с id = '{config.default_id}' не найдена.",
                                             'Обновление колонки с неверным ID успешно осуществилось')

        #обновить колонку не передав name
        update_noname = MyRequests.put(f'/tm_reports/api/ReportColumn/{self.report_column_id}', headers={'Content-Type': 'application/json'},
                                             data=self.update_noname)
        Assertions.assert_json_value_by_name(update_noname, 'Message', 'Name - обязательный параметр.','Обновление колонки без name успешно осуществилось')

        #обновить колонку не передав jsonPathFromProcessContext
        update_nojsonpath = MyRequests.put(f'/tm_reports/api/ReportColumn/{self.report_column_id}', headers={'Content-Type': 'application/json'},
                                             data=self.update_nojsonpath)
        Assertions.assert_json_value_by_name(update_nojsonpath, 'Message', 'JsonPathFromProcessContext - обязательный параметр.',
                                             'Обновление колонки без JsonPathFromProcessContext успешно осуществилось')

        #обновить колонку с дублем name
        update_dublicate_name =  MyRequests.put(f'/tm_reports/api/ReportColumn/{self.report_column_id_second}', headers={'Content-Type': 'application/json'},
                                             data=self.update_dublicate_name)
        Assertions.assert_json_value_by_name(update_dublicate_name, 'Message', f"Колонка с именем 'Column Test' для отчета '{self.report_id}' уже существует.",
                                             'Обновление колонки с дублем Name успешно осуществилось')

        #обновить колонку с дублем jsonpath
        update_dublicate_jsonpath = MyRequests.put(f'/tm_reports/api/ReportColumn/{self.report_column_id}', headers={'Content-Type': 'application/json'},
                                             data=self.update_dublicate_jsonpath)
        Assertions.assert_json_value_by_name(update_dublicate_jsonpath, 'Message', f"Колонка с json_path '$.lpu.address.second' для отчета '{self.report_id}' уже существует.",
                                             'Обновление колонки с дублем JsonPathFromProcessContext успешно осуществилось')

        #запросить колонку с некорректным id
        get_incorrectId = MyRequests.get(f'/tm_reports/api/ReportColumn/{config.default_id}')
        Assertions.assert_json_value_by_name(get_incorrectId, 'Message', f"Колонка с id = '{config.default_id}' не найдена.",
                                             'Ошибка, что Id не найден не получена')

        #удаление колонки с некорректным id
        delete_incorrectId = MyRequests.delete(f'/tm_reports/api/ReportColumn/{config.default_id}')
        Assertions.assert_json_value_by_name(delete_incorrectId, 'Message', f"Колонка с id = '{config.default_id}' не найдена.",
                                             'Ошибка, что Id не найден не получена')

        #получение списка колонок по некорректному id отчёта
        get_columns_incorrectId = MyRequests.get(f'/tm_reports/api/ReportColumn/GetReportColumnByReportId/{config.default_id}')
        Assertions.assert_json_value_by_name(get_columns_incorrectId, 'Message', f"Отчет с id = '{config.default_id}' не найден.",
                                             'Ошибка, что Id не найден не получена')

    @allure.feature("Тесты на CRUD колонки отчёта")
    def test_crud_report_columns(self):

        #создание колонки
        create = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.create)
        Assertions.assert_code_status(create, 200)

        column_id = create.json()['id']

        #получить колонку по ID
        get_column = MyRequests.get(f'/tm_reports/api/ReportColumn/{column_id}')
        Assertions.assert_json_value_by_name(get_column, 'id', column_id, 'Полученная колонка не равна ожидаемой')

        #обновить колонку
        update = MyRequests.put(f'/tm_reports/api/ReportColumn/{column_id}', headers={'Content-Type': 'application/json'}, data=self.update)
        Assertions.assert_json_value_by_name(update, 'name', 'Column Autotest Update', 'Имя колонки после обновления не равно ожидаемому')
        Assertions.assert_json_value_by_name(update, 'jsonPath', '$.lpu.update', 'JsonPath после обновления не равен ожидаемому')

        #увидеть колонку в ответе GetReportColumnByReportId
        get_columns = MyRequests.get(f'/tm_reports/api/ReportColumn/GetReportColumnByReportId/{self.report_id}')
        s = 0
        for i in range(len(get_columns.json())):
            if get_columns.json()[i]['id'] == column_id:
                s += 1
        assert s == 1, 'Созданная колонка не находится среди колонок отчета'

        #удалить колонку
        delete = MyRequests.delete(f'/tm_reports/api/ReportColumn/{column_id}')
        Assertions.assert_expectedvalue_equal_receivedvalue(delete, delete.text, f"Колонка {column_id} удалена.", 'Удаление колонки прошло неуспешно')

@allure.epic("Полноценные проверки ReportTemplate")
class TestReportTemplate(BaseCase):

    def setup(self):

        self.reporttemplateid = "1c377655-fb99-4fbb-8686-54559c698fbf"

        self.noname = "{\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.dublicate_name = "{\"name\":\"template usual\",\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.notemplateView = "{\"name\":\"12345\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.notemplateType = "{\"name\":\"12345\",\"templateView\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.norequestBody = "{\"name\":\"12345\",\"templateView\":\"1\",\"templateType\":\"1\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.nocolumnView = "{\"name\":\"12345\",\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.nofilterPreset = "{\"name\":\"12345\",\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.noreportId = "{\"name\":\"12345\",\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\"}"
        self.search_incorrect_id = "{\"reportId\": \"3fa85f64-5717-4562-b3fc-2c963f66afa6\"}"

        self.create = "{\"name\":\"autotest\",\"templateView\":\"1\",\"templateType\":\"1\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.update = "{\"name\":\"autotest update\",\"templateView\":\"2\",\"templateType\":\"2\",\"requestBody\":\"{}\",\"columnsView\":\"{}\",\"filterPreset\":\"{}\",\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"
        self.getbyfilter = "{\"pageNumber\":1,\"pageSize\":10,\"reportId\":\"3bd98022-68da-400e-b780-cd403a72cda7\"}"

    @allure.feature("Негативные тесты на шаблон отчёта")
    def test_negative_reporttemplate(self):

        #создание без name
        create_noname = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.noname)
        Assertions.assert_json_value_by_name(create_noname, 'Message', 'Name - обязательный параметр.','Ожидаемая ошибка об отсутствии Name не получена')

        #создание с дублем имени
        create_dulicate_name = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.dublicate_name)
        Assertions.assert_json_value_by_name(create_dulicate_name, 'Message', "Шаблон отчета с именем 'template usual' уже существует.",
                                             'Ожидаемая ошибка о дубликате Name не получена')

        #создание без templateView
        create_notemplateView = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.notemplateView)
        Assertions.assert_json_value_by_name(create_notemplateView, 'Message', 'TemplateView - обязательный параметр и не может быть Default.',
                                             'Ожидаемая ошибка об отсутствии TemplateView не получена')

        #создание без templateType
        create_notemplateType = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.notemplateType)
        Assertions.assert_json_value_by_name(create_notemplateType, 'Message', 'TemplateType - обязательный параметр и не может быть Default.',
                                             'Ожидаемая ошибка об отсутствии TemplateType не получена')

        #создание без requestBody
        create_norequestBody = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.norequestBody)
        Assertions.assert_json_value_by_name(create_norequestBody, 'Message', 'RequestBody - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии RequestBody не получена')

        #создание без columnsView
        create_nocolumnView = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.nocolumnView)
        Assertions.assert_json_value_by_name(create_nocolumnView, 'Message', 'ColumnsView - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии ColumnsView не получена')

        #создание без filterPreset
        create_nofilterPreset = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.nofilterPreset)
        Assertions.assert_json_value_by_name(create_nofilterPreset, 'Message', 'FilterPreset - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии FilterPreset не получена')

        #создание без reportId
        create_noreportId = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.noreportId)
        Assertions.assert_json_value_by_name(create_noreportId, 'Message', 'ReportId - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии ReportId не получена')

        #обновление без name
        update_noname = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.noname)
        Assertions.assert_json_value_by_name(update_noname, 'Message', 'Name - обязательный параметр.','Ожидаемая ошибка об отсутствии Name не получена')

        #обновление с дублем имени
        update_dulicate_name = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.dublicate_name)
        Assertions.assert_json_value_by_name(update_dulicate_name, 'Message', "Шаблон отчета с именем 'template usual' уже существует.",
                                             'Ожидаемая ошибка о дубликате Name не получена')

        #обновление с неверным ID
        update_incorrect_id = MyRequests.put(f'/tm_reports/api/ReportTemplate/{config.default_id}', headers={'Content-Type': 'application/json'}, data=self.dublicate_name)
        Assertions.assert_json_value_by_name(update_incorrect_id, 'Message', f"Шаблон отчета с id = '{config.default_id}' не найден.",
                                             'Ожидаемая ошибка о неверном ID не получена')

        #обновление без templateView
        update_notemplateView = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.notemplateView)
        Assertions.assert_json_value_by_name(update_notemplateView, 'Message', 'TemplateView - обязательный параметр и не может быть Default.',
                                             'Ожидаемая ошибка об отсутствии TemplateView не получена')

        #обновление без templateType
        update_notemplateType = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.notemplateType)
        Assertions.assert_json_value_by_name(update_notemplateType, 'Message', 'TemplateType - обязательный параметр и не может быть Default.',
                                             'Ожидаемая ошибка об отсутствии TemplateType не получена')

        #обновление без requestBody
        update_norequestBody = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.norequestBody)
        Assertions.assert_json_value_by_name(update_norequestBody, 'Message', 'RequestBody - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии RequestBody не получена')

        #обновление без columnsView
        update_nocolumnView = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.nocolumnView)
        Assertions.assert_json_value_by_name(update_nocolumnView, 'Message', 'ColumnsView - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии ColumnsView не получена')

        #обновление без filterPreset
        update_nofilterPreset = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.nofilterPreset)
        Assertions.assert_json_value_by_name(update_nofilterPreset, 'Message', 'FilterPreset - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии FilterPreset не получена')

        #обновление без reportId
        update_noreportId = MyRequests.put(f'/tm_reports/api/ReportTemplate/{self.reporttemplateid}', headers={'Content-Type': 'application/json'}, data=self.noreportId)
        Assertions.assert_json_value_by_name(update_noreportId, 'Message', 'ReportId - обязательный параметр.',
                                             'Ожидаемая ошибка об отсутствии ReportId не получена')

        #получение шаблона по некорректному ID
        get_incorrect_id = MyRequests.get(f'/tm_reports/api/ReportTemplate/{config.default_id}')
        Assertions.assert_json_value_by_name(get_incorrect_id, 'Message', f"Шаблон отчета с id = '{config.default_id}' не найден.", "Ошибка о неверном ID не получена")

        #удаление шаблона по некорректному ID
        delete_incorrect_id = MyRequests.delete(f'/tm_reports/api/ReportTemplate/{config.default_id}')
        Assertions.assert_json_value_by_name(delete_incorrect_id, 'Message',f"Шаблон отчета с id = '{config.default_id}' не найден.", "Ошибка о неверном ID не получена")

        #поиск по некорректному ID
        search_incorrect_id = MyRequests.post('/tm_reports/api/ReportTemplate/GetByFilter', headers={'Content-Type': 'application/json'},
                                              data=self.search_incorrect_id)
        Assertions.assert_json_value_by_name(search_incorrect_id, 'count', 0, 'Информация по некорректному ID найдена')

    @allure.feature("CRUD тесты на шаблон отчёта")
    def test_crud_reporttemplate(self):

        #создание шаблона отчёта
        create = MyRequests.post('/tm_reports/api/ReportTemplate', headers={'Content-Type': 'application/json'}, data=self.create)
        Assertions.assert_json_value_by_name(create, 'templateView', 'MedicalOrganization', 'Значение templateView не равно ожидаемому')
        Assertions.assert_json_value_by_name(create, 'templateType', 'List', 'Значение templateType не равно ожидаемому')

        report_template_id = create.json()['id']

        #обновление шаблона (templateView и templateType)
        update = MyRequests.put(f'/tm_reports/api/ReportTemplate/{report_template_id}', headers={'Content-Type': 'application/json'}, data=self.update)
        Assertions.assert_json_value_by_name(update, 'templateView', 'Regional', 'Значение templateView не равно ожидаемому')
        Assertions.assert_json_value_by_name(update, 'templateType', 'Aggregate', 'Значение templateType не равно ожидаемому')

        #получить шаблон отчёта
        get = MyRequests.get(f'/tm_reports/api/ReportTemplate/{report_template_id}')
        Assertions.assert_json_value_by_name(get, 'name', 'autotest update', 'Полученный шаблон не равен ожидаемому')

        #найти шаблон среди данных отчёта
        getbyfilter = MyRequests.post('/tm_reports/api/ReportTemplate/GetByFilter', headers={'Content-Type': 'application/json'}, data=self.getbyfilter)

        array_template = getbyfilter.json()['reportTemplates']
        Assertions.assert_expectedvalue_equal_receivedvalue(getbyfilter, getbyfilter.json()['count'], len(array_template),
                                                            'Количество шаблонов по отчёту не сходится')
        s = 0
        for i in range(len(array_template)):
            if array_template[i]['id'] == report_template_id:
                s += 1
        Assertions.assert_expectedvalue_equal_receivedvalue(getbyfilter, 1, s, 'Созданный шаблон отчёта не находится в ответе GetByFilter по этому отчёту')

        #удалить шаблон отчёта
        delete = MyRequests.delete(f'/tm_reports/api/ReportTemplate/{report_template_id}')
        Assertions.assert_expectedvalue_equal_receivedvalue(delete, delete.text, f"Шаблон отчета c id = '{report_template_id}' удален.",
                                                            'Удаление шаблона отчёта прошло неуспешно')