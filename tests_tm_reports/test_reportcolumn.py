import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки ReportColumn")
class TestReportColumn(BaseCase):
    def setup(self):

        self.noreportId = "{'name':'Адрес МО','jsonPathFromProcessContext':'$.lpu.address','type':1}".encode('UTF-8')

    @allure.feature("Негативные тесты на колонку")
    def test_negative_reportcolumn(self):

        noreportId = MyRequests.post('/tm_reports/api/ReportColumn', headers={'Content-Type': 'application/json'}, data=self.noreportId)
        Assertions.assert_json_value_by_name(noreportId, 'Message', 'ReportId - обязательный параметр.', noreportId.json()['Message'])