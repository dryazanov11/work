import datetime

import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Template")
class TestTemplate(BaseCase):

    def setup(self):
        self.noname = "{'templateTypeName':'Очередь','active':true,'templateIntervals':[{'dayOfWeekStart':1,'dayOfWeekEnd':3,'startTime':'10:00','endTime':'14:00','limit':10}]}".encode('UTF-8')
        self.dublicate_name = "{'name': 'Шаблон для автотестов','templateTypeName':'Очередь','active':true,'templateIntervals':[{'dayOfWeekStart':1,'dayOfWeekEnd':3,'startTime':'10:00','endTime':'14:00','limit':10}]}".encode('UTF-8')
        self.notemplatetypename = "{'name': 'test-0107','active':true,'templateIntervals':[{'dayOfWeekStart':1,'dayOfWeekEnd':3,'startTime':'10:00','endTime':'14:00','limit':10}]}"
        self.notemplateintervals = "{'name': 'test-0107','templateTypeName':'Очередь','active':true}".encode('UTF-8')
        self.nolimit = "{'name': 'test-0107','templateTypeName':'Очередь','active':true,'templateIntervals':[{'dayOfWeekStart':1,'dayOfWeekEnd':3,'startTime':'10:00','endTime':'14:00'}]}".encode('UTF-8')

    @allure.feature("Создание шаблона не передавая обязательные параметры")
    def test_create_template_negative(self):

        #без name
        noname = MyRequests.post('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'}, data=self.noname)
        Assertions.assert_json_value_by_name(noname, 'message', 'Название шаблона не должно быть пустым', 'Текст ошибки при отсутствии name не равен ожидаемому')

        #повтор названия
        dublicate_name = MyRequests.post('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'}, data=self.dublicate_name)
        Assertions.assert_json_value_by_name(dublicate_name, 'message', "Название шаблона 'Шаблон для автотестов' не уникально", 'Текст ошибки при дубликате name не равен ожидаемому')

        #без templateTypeName
        notemplatetypename = MyRequests.post('/tm-schedule/api/templates',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.notemplatetypename)
        Assertions.assert_json_value_by_name(notemplatetypename, 'message','Тип шаблона не указан','Текст ошибки при отсутствии templateTypeName не равен ожидаемому')

        #без templateIntervals
        notemplateintervals = MyRequests.post('/tm-schedule/api/templates',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.notemplateintervals)
        Assertions.assert_json_value_by_name(notemplateintervals, 'message','Интервалы шаблона не заданы','Текст ошибки при отсутствии templateIntervals не равен ожидаемому')

        #без limit
        nolimit = MyRequests.post('/tm-schedule/api/templates',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.nolimit)
        Assertions.assert_json_value_by_name(nolimit, 'message','Максимальное количество возможных записей не указано','Текст ошибки при отсутствии limit не равен ожидаемому')

        #без startTime и endTime кривая ошибка "message": "Value cannot be null. (Parameter 'input')\n" - ДОБАВИТЬ ЗАДАЧУ И ГЛЯНУТЬ ДОПОЛНИТЕЛЬНО ДРУГИЕ ЗАПРОСЫ
        #у fhir создания шаблона ошибка тоже кривая Nullable object must have a value.

