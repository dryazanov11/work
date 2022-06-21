import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки TM.Widgets")
class TestTmWidgets(BaseCase):

    #часть проверок в test_check_method

    @allure.feature("Проверка связи с MPI")
    def test_tm_widgets_mpi(self):
        response = MyRequests.get('/tm-widgets/api/mpi/SearchPatientById?patientId=f99f8a26-37f2-4a66-818f-1dae64e8d490', headers={'accept': 'text/plain'})
        Assertions.assert_json_value_by_name(response,'resourceType', 'Patient', 'Карточку пациента получить не удалось')
        Assertions.assert_code_status(response, 200)

    #Для проверки сервиса permissionStore  нужно выполнить метод /api/Agreement, на выход передать идентификатор ЕСИА пациента и идентификатор МО из 64 справочника - НЕТ ДАННЫХ ЕСИА

    #Для Ириды - /api/Irida/chats/unreaded - запросить по заренее подготовленному со стороны Ириды чату - НАЙТИ ЧАТ

    @allure.feature("Проверка organizationsService")
    def test_tm_widgets_org_serv(self):
        response = MyRequests.get(f'/tm-widgets/api/organizations/byAttachment?idMpi={config.patientId}')
        Assertions.assert_json_value_by_name(response, 'success', True, 'Не удалось получить список организаций пациента по прикреплению')
        Assertions.assert_code_status(response, 200)


