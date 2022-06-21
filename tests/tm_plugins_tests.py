
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки TM.Plugins")
class TestTmPlugins(BaseCase):

    #не понял как проверить: humanFriendlyIdPrefix должен быть равен "TMC" для проекта "телемедицина"

    @allure.feature("Проверка связи tm.plugins с tm.core")
    def test_tm_plugins_to_tm_core(self):
        response = MyRequests.get('/tm-plugins/pingTmCore')
        Assertions.assert_json_value_by_name(response, 'success', True, 'Проверка соединения TM.Plugins с TM.Core прошла неуспешно')
        Assertions.assert_code_status(response, 200)

    @allure.feature("Проверка подключения к БД")
    def test_tm_plugins_to_db(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=config.request_dublicate.encode('UTF-8'))
        Assertions.assert_json_value_by_name(response, 'message', 'По данной заявке найден дубль TMC0522X7HI19', 'Проверка на дубликат пройдена неуспешно')
        Assertions.assert_code_status(response, 200)

    # @allure.feature("Проверка mass_transit_queue")
    # def test_tm_plugins_mtq(self):
    #     response = MyRequests.post('/tm-plugins/Callbacks/ProcessStarted')
        #не понял как проверить очередь - Для проверки mass_transit_queue выполнить метод /Callbacks/ProcessStarted и убедиться что в очередь ЕЭМК пришло уведомление

    #не понял как это проверить с помощью очереди уведомлений - Для проверки subscription нужно повесить на один из переходов бизнеспроцесса колбэк /Callbacks /CheckEmergencyParameterValue и убедиться что он приходит в очередь уведомлений

    @allure.feature("Проверка настроек MPI")
    def test_tm_plugins_mpi(self):
        response = MyRequests.get(f'/tm-plugins/api/Mpi/GetPatientCardById/{config.patientId}', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})
        Assertions.assert_json_has_not_key(response, 'message')
        Assertions.assert_code_status(response, 200)

    #не понял что передать и что ожидать в ответе - Для проверки связи со справочниками НСИ - выполнить метод /api/PresenceParameterValueValidator/PresenceParameterValueValidator

    #@allure.feature("Проверка связи с СЗПВ")
    #def test_tm_plugins_szpv(self):
        #нужен верный урл

    #@allure.feature("Проверка связи с Иридой")
        #def test_tm_plugins_irida(self):
           #нужен верный чат

    #Для tm.settings - нужно выполнить метод /api/Workflow/GetFullWorkflow/{workflowId} (предварительно у выбранного маршрута должны быть настроены формы) - ЧТО КОНКРЕТНО ТУТ ПРОВЕРЯЕТСЯ?

