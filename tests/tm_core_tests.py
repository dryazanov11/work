import json

import datetime
import time
from datetime import date
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки TM.Core")
class TestTmCore(BaseCase):

    def setup(self):

        self.request_startnewprocess = "{'WorkflowId':'5deb701e-b987-41a7-874c-5daf9a6afcc7','Name':'Тест профиля','InitialTransitionId':'f4a18d8f-8f15-4b98-a924-5a21e30d666b','ProcessContext':{'a':'1','b':'1','profile':{'id':'157e1b81-c3e3-456f-8eb3-a73e8b8175a7'},'serviceRequest':{'REGIS':[{'id':'17','code':'69161b26-7aca-4562-8878-42958e2733ce','system':'1.2.643.2.69.1.2.110','isDeleted':false}],'healthCareService':'98a73ea7-ce26-45a6-bab7-199be88d25e9'},'patient':{'telecom':[{'id':'1','value':'+79681819712','system':'1'}],'name':{'LastName':'Тестов','FirstName':'Тест'},'idMPI':'689ae90d-8779-4005-a443-1cee7d24e719'},'EventsInfo':{'Source':{'ReferralCreateDate':'2022-04-15T10:00:00+03:00','ReferralOutDate':'2022-04-15T10:00:00+03:00'}}},'roleContext':{'bf2e0147-ec85-489c-bd88-52331b0dc013':{'SNILS':'1','idLpu':'1'},'2a3c7729-1d9f-4284-ab7d-442b08293905':{'idLpu':'1'}}}".encode('UTF-8')
        self.request_getoverduestages = "{'ProcessCreatedDateFrom': 'date_from', 'ProcessCreatedDateTo': 'date_to', 'ProcessIds': ['processid_overdue'], 'Take': 10, 'OrderByCreationDate': true, 'DescendingOrder': true}"
        self.request_movetostage = "{'processId': 'processid_mts', 'Name': 'Тест профиля', 'transitionId': '42f6865d-7e9f-47d6-b39b-2fe3e64df654', 'ProcessContext': {'a': '1', 'b': '1', 'profile': {'id': '157e1b81-c3e3-456f-8eb3-a73e8b8175a7'}, 'serviceRequest': {'REGIS': [{'id': '17', 'code': '69161b26-7aca-4562-8878-42958e2733ce', 'system': '1.2.643.2.69.1.2.110', 'isDeleted': false}], 'healthCareService': '98a73ea7-ce26-45a6-bab7-199be88d25e9'}, 'patient': {'telecom': [{'id': '1', 'value': '+79681819712', 'system': '1'}], 'name': {'LastName': 'Тестов', 'FirstName': 'Тест'}, 'idMPI': '689ae90d-8779-4005-a443-1cee7d24e719'}, 'EventsInfo': {'Source': {'ReferralCreateDate': '2022-04-15T10:00:00+03:00', 'ReferralOutDate': '2022-04-15T10:00:00+03:00'}}}, 'roleContext': {'bf2e0147-ec85-489c-bd88-52331b0dc013': {'SNILS': '1', 'idLpu': '1'}, '2a3c7729-1d9f-4284-ab7d-442b08293905': {'idLpu': '1'}}}"
        self.request_stage_timeout = "{'workflowId':'9671ed97-3951-4713-bc2d-b0f68c1f5263','name':'Тестовая заявка на просрочку','initialTransitionId':'c1bb3b76-d776-48de-af90-ad96f64c4850','processContext':{'patient':{'idMPI':'689ae90d-8779-4005-a443-1cee7d24e719','fullName':'Березовский Андрей Валерьевич'},'appointment':{'end':'09.11.2022, 12:24:41','start':'09.11.2022, 11:24:41'},'presentedForm':{'fileURL':'https://r78-rc.tm.zdrav.netrika.ru/download?file=990','signatureURL':'https://r78-rc.tm.zdrav.netrika.ru/download?file=991','filenameExtension':'pdf','cdaVersion':'5'},'serviceRequest':{'category':'120','performerOrganization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','requesterOrganization':'6c34dc18-cab0-4e53-aba8-cea197f0ab5e','reasonCode':'9'},'diagnosticReport':{'conclusion':'Здорова','idCaseAidType':'A12.06.062','documentNumber':'TMK_123'},'performerPractitioner':{'telecom':{'email':'test@mail.ru','phone':'89129328345'},'fullName':'Городыский Виктор Георгиевич','position':'4','specialty':'124','department':'8bbb2c42-77b1-4c75-97aa-0af48dc15238','identityDocument':{'code':'00861254229','system':'223'}}},'roleContext':{}}".encode('UTF-8')
        self.request_metadata = "{'WorkflowId':'db648adb-aa34-4b08-a4b0-e4a11a6b9e44','Name':'РўРµСЃС‚ РїСЂРѕС„РёР»СЏ','InitialTransitionId':'c63356eb-092e-4b3d-a9e1-9059ae94bad6','ProcessContext':{'patient':{'idMPI':'00882d8f-7286-4d09-b1e9-649343d9d690','gender':'1','fullName':'Р СЏСЃРЅРѕРІР°  Р•Р»РµРЅР°  Р’РёРєС‚РѕСЂРѕРІРЅР° ','birthDate':'1992-03-15','identityDocument':{'code':'1111:858445','system':'14'},'registeredInTheRegion':false},'appointment':{'requestedPeriod':{'end':'16:45','start':'16:45'}},'attachedfiles':[],'serviceRequest':{'REGIS':[],'urgency':'3','category':'4','reasonCode':'9','primaryAppeal':'','performerOrganization':'4107450a-67a2-e4a4-ac5d-688cb9c3b70f','requesterOrganization':'4107450a-67a2-e4a4-ac5d-688cb9c3b70f'},'requesterCondition':{'codeMKB':'Z00.6','anamnesis':'С‚РµСЃС‚','complaints':'С‚РµСЃС‚2'},'requesterPractitioner':{'telecom':{'email':'','phone':'111-00-99'},'fullName':'РќР°РїСЂР°РІР»СЏСЋС‰РёР№ Р’СЂР°С‡','position':'4','specialty':'','department':'9605b65a-259d-4b1e-9695-21773a8febde','identityDocument':{'code':'00000000002','system':'223'}}},'roleContext':{'c7ec2fc0-982c-4ec1-ae84-c7ec1347ddfb':{'idMPI':'689ae90d-8779-4005-a443-1cee7d24e719','idIP':'00000000-0000-0000-2222-000000000000'}}}".encode('UTF-8')

    #в проверках запросы используются для dev стенда
    def test_connect_to_rabbit(self):

        #создаю заявку
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess',headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},data=self.request_startnewprocess)

        #беру из ответа processid
        processId = self.get_json_value(response, 'processId')

        #проверка humanFirendlyId, что есть в ответе
        Assertions.assert_json_has_key(response, 'humanFriendlyId')
        Assertions.assert_code_status(response, 200)

        #в запрос из конфиг вставляю processId
        self.request_movetostage = self.request_movetostage.replace('processid_mts', f'{processId}')

        #меняю статус заявки
        response1 = MyRequests.post('/tm-core/api/Commands/MoveToStage',
                                    headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'}, data=self.request_movetostage.encode('UTF-8'))
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_expectedvalue_equal_receivedvalue(response1, processId, response1.json()['processId'], 'Запрос MoveToStage неуспешен')

        #В результате в очереди рэббита должны появиться соответствующие уведомления
        #Предполагаю, что речь идет о http://10.62.1.27:15672/#/queues/tmcore/createdProcess и http://10.62.1.27:15672/#/queues/tmcore/moveToStage, надо понять как там проверить появление уведомлений

    #def test_check_maxPageSize(self):
        #Для проверки maxPageSize использовать какой-то запрос, который может вернуть более указанного в этом поле количества записей. Убедится что количество не больше указанного значения

    def test_worker(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=self.request_stage_timeout)  #создаю заявку

        Assertions.assert_json_has_key(response, 'processId')
        Assertions.assert_code_status(response, 200)

        time.sleep(60)  #жду наступления просрочки

        processId = self.get_json_value(response, 'processId')

        #в запрос из конфиг вставляю новые значения
        replace_values = {'date_from': str(date.today()), 'date_to': str(date.today() + datetime.timedelta(days=1)), 'processid_overdue': processId}
        self.request_getoverduestages = self.multiple_replace(self.request_getoverduestages, replace_values)

        #делаю запрос на получение просрочек и ожидаю получить одну
        response1 = MyRequests.post('/tm-core/api/Queries/GetOverdueStages', headers ={'Content-Type': 'application/json', 'Authorization': f'{config.headers}'},
                                    data=self.request_getoverduestages.encode('UTF-8'))

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_expectedvalue_equal_receivedvalue(response1, response1.json()['result']['total'], 1, "Просрочки нет")

    def test_metadata(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=self.request_metadata)  #создаю заявку

        processId = self.get_json_value(response, 'processId')

        response1 = MyRequests.get(f'/tm-core/api/Queries/GetProcess/{processId}',
                                   headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})  #получение заявки по id

        Assertions.assert_expectedvalue_equal_receivedvalue(response1, response1.json()['result']['metadata']['scopedMetadata']['Целевая организация'],
                                                           '4107450a-67a2-e4a4-ac5d-688cb9c3b70f', 'Значение целевой МО не соответствует ожидаемому')  #проверки, что значения в ответе будут соответствовать ожидаемым
        Assertions.assert_expectedvalue_equal_receivedvalue(response1, response1.json()['result']['metadata']['scopedMetadata']['Профиль медицинской помощи, по которому запрашивается консультация'],
                                                           '4', 'Значение профиля не соответствует ожидаемому')

    def test_access_check(self):
        #получить ответ false

        response = MyRequests.get('/tm-core/api/Queries/access/check?idMpi=689ae90d-8779-4005-a443-1cee7d24e719&doctorSnils=48368377143', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})
        if response.json()['result']['hasAccess'] == 'True':
            print('Проверка доступа привела к успеху, тогда как должна была быть неудача')

        #нужно понять с какими данными обращаться к методу, пока не смог получить true ответ








