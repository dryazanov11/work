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
    def test_connect_to_rabbit(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess',
                                   headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=config.request_startnewprocess.encode('UTF-8'))  #создаю заявку

        processId = self.get_json_value(response, 'processId')  #беру из ответа processid

        Assertions.assert_json_has_key(response, 'humanFriendlyId')  #проверка humanFirendlyId, что есть в ответе
        Assertions.assert_code_status(response, 200)

        with open(r"C:\Users\User\Desktop\work\tests\request_movetostage.txt", 'r', encoding='UTF-8') as f:  #открываю файл запроса и записываю в него processId, полученный ранее
            json_data = json.load(f)
            json_data['processId'] = processId
        with open(r"C:\Users\User\Desktop\work\tests\request_movetostage.txt", 'w', encoding='UTF-8') as f:
            f.write(json.dumps(json_data, ensure_ascii=False))

        json_data = json.dumps(json_data).encode('UTF-8')  #из dict перевожу в bytes, чтобы метод схавал такую data

        response1 = MyRequests.post('/tm-core/api/Commands/MoveToStage',
                                    headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'}, data=json_data) #меняю статус заявки
        Assertions.assert_code_status(response1, 200)

        #В результате в очереди рэббита должны появиться соответствующие уведомления
        #Предполагаю, что речь идет о http://10.62.1.27:15672/#/queues/tmcore/createdProcess и http://10.62.1.27:15672/#/queues/tmcore/moveToStage, надо понять как там проверить появление уведомлений

    #def test_check_maxPageSize(self):
        #Для проверки maxPageSize использовать какой-то запрос, который может вернуть более указанного в этом поле количества записей. Убедится что количество не больше указанного значения

    def test_worker(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess',
                                   headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=config.request_stage_timeout.encode('UTF-8'))  #создаю заявку

        Assertions.assert_json_has_key(response, 'processId')
        Assertions.assert_code_status(response, 200)

        time.sleep(60)  #жду наступления просрочки

        processId = self.get_json_value(response, 'processId')

        with open(r"C:\Users\User\Desktop\work\tests\request_getoverduestages.txt", 'r', encoding='UTF-8') as f:  #записываю в новый запрос по поиску просрочек актуальные данные
            json_data = json.load(f)
            json_data['ProcessIds'][0] = processId
            json_data['ProcessCreatedDateFrom'] = str(date.today())
            json_data['ProcessCreatedDateTo'] = str(date.today() + datetime.timedelta(days=1))
        with open(r"C:\Users\User\Desktop\work\tests\request_getoverduestages.txt", 'w', encoding='UTF-8') as f:
            f.write(json.dumps(json_data, ensure_ascii=False))

        json_data = json.dumps(json_data).encode('UTF-8')  #из dict перевожу в bytes, чтобы метод схавал такую data

        response1 = MyRequests.post('/tm-core/api/Queries/GetOverdueStages',
                                    headers ={'Content-Type': 'application/json', 'Authorization': f'{config.headers}'},
                                    data=json_data)  #делаю запрос на получение просрочек и ожидаю получить одну

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_expectedvalue_equal_recivedvalue(response1, response1.json()['result']['total'], 1, "Просрочки нет")

    def test_metadata(self):
        response = MyRequests.post('/tm-core/api/Commands/StartNewProcess', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'},
                                   data=config.request_metadata.encode('UTF-8'))  #создаю заявку

        processId = self.get_json_value(response, 'processId')

        response1 = MyRequests.get(f'/tm-core/api/Queries/GetProcess/{processId}',
                                   headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})  #получение заявки по id

        Assertions.assert_expectedvalue_equal_recivedvalue(response1, response1.json()['result']['metadata']['scopedMetadata']['Целевая организация'],
                                                           '4107450a-67a2-e4a4-ac5d-688cb9c3b70f', 'Значение целевой МО не соответствует ожидаемому')  #проверки, что значения в ответе будут соответствовать ожидаемым
        Assertions.assert_expectedvalue_equal_recivedvalue(response1, response1.json()['result']['metadata']['scopedMetadata']['Профиль медицинской помощи, по которому запрашивается консультация'],
                                                           '4', 'Значение профиля не соответствует ожидаемому')

    def test_access_check(self):
        #получить ответ false

        response = MyRequests.get('/tm-core/api/Queries/access/check?idMpi=689ae90d-8779-4005-a443-1cee7d24e719&doctorSnils=48368377143', headers ={'Content-Type': 'application/json','Authorization': f'{config.headers}'})
        if response.json()['result']['hasAccess'] == 'True':
            print('Проверка доступа привела к успеху, тогда как должна была быть неудача')

        #нужно понять с какими данными обращаться к методу, пока не смог получить true ответ








