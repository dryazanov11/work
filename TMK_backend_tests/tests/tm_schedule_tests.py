
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки TM.Schedule")
class TestTmSchedule(BaseCase):

    @allure.feature("Проверка получения активных маршрутов")
    def test_tm_schedule_getworkflows(self):
        response = MyRequests.get('/tm-schedule/api/tmCore/getWorkflows?isDisabled=false', headers={'accept': 'text/plain', 'Authorization': f'{config.token_dev_schedule}'})
        Assertions.assert_json_value_by_name(response,'success', True, 'Метод ответил неуспешно')
        Assertions.assert_code_status(response, 200)

    #не оч понял о чем речь
    #Чтобы проверить, правильно ли указан workflowOid нужно создать конфигурацию параметра профиля с этим значением, создать профиль, используя этот параметр, в ТМК создать заявку, которая будет запускать метод "profiles/available". При соответствии параметров профиля и заявки валидатор будет возвращать true (Отказаться от параметра workflowOid и добавить для профиля свойство "workflowOid")

    @allure.feature("Проверка связи с NSI")
    def test_tm_schedule_nsi(self):
        response = MyRequests.get('/tm-schedule/api/schedules/nsi', headers={'accept': 'text/plain', 'Authorization': f'{config.token_dev_schedule}'})
        Assertions.assert_json_value_by_name(response, 'success', True, 'Метод ответил неуспешно')
        Assertions.assert_code_status(response, 200)

