
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки TM.Plugins")
class TestTmPlugins(BaseCase):

    def setup(self):

        self.request_dublicate = "{'WorkflowId':'9671ed97-3951-4713-bc2d-b0f68c1f5263','Name':'Тест на дубликат','InitialTransitionId':'f8e5ab2a-5f15-4b70-9aef-cb0851d58624','ProcessContext':{'profile':{'id':'db0a9ae7-0ced-4d1c-958f-3d63cb9295fb'},'patient':{'idMPI':'689ae90d-8779-4005-a443-1cee7d24e719','gender':'1','fullName':'Иванов Иван Иванович','birthDate':'1992-03-15','identityDocument':{'code':'1111:858445','system':'14'},'registeredInTheRegion':false},'appointment':{'requestedPeriod':{'end':'16:45','start':'16:45'}},'attachedfiles':[],'serviceRequest':{'REGIS':[{'id':'1','code':'11161b26-7aca-4562-8878-42958e270001','system':'1.2.643.2.69.1.2.110','isDeleted':false},{'id':'2','code':'11161b26-7aca-4562-8878-42958e273113','system':'1.2.643.2.69.1.2.110','isDeleted':false}],'healthCareService':'db0a9ae7-0ced-4d1c-958f-3d63cb9295fb','urgency':'3','category':'100','reasonCode':'9','primaryAppeal':'','performerOrganization':'691435a4-d379-453f-b3a8-0f18a679a44b','requesterOrganization':'691435a4-d379-453f-b3a8-0f18a679a44b','typeOfServiceProvision':'1','nomenclatureOfMedicalServices':'A08.30.018'},'requesterCondition':{'codeMKB':'Z00.6','anamnesis':'болезнь','complaints':'рана'},'requesterPractitioner':{'telecom':{'email':'','phone':'111-00-99'},'fullName':'Тестов Тест Тестович','position':'4','specialty':'','department':'9605b65a-259d-4b1e-9695-21773a8febde','identityDocument':{'code':'00000000002','system':'223'}}},'roleContext':{'5ff16ba7-9edd-41a4-bd06-2ee33cfd4597':{'organization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','SNILS':'48368377143'},'c7ec2fc0-982c-4ec1-ae84-c7ec1347ddfb':{'idMPI':'689ae90d-8779-4005-a443-1cee7d24e719','idIP':'00000000-0000-0000-2222-000000000000'}}}".encode('UTF-8')

    #не понял как проверить: humanFriendlyIdPrefix должен быть равен "TMC" для проекта "телемедицина"

    @allure.feature("Проверка связи tm.plugins с tm.core")
    def test_tm_plugins_to_tm_core(self):
        response = MyRequests.get('/tm-plugins/pingTmCore')
        Assertions.assert_json_value_by_name(response, 'success', True, 'Проверка соединения TM.Plugins с TM.Core прошла неуспешно')
        Assertions.assert_code_status(response, 200)

    @allure.feature("Проверка подключения к БД")
    def test_tm_plugins_to_db(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},data=self.request_dublicate)
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

