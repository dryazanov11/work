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
        self.incorrectid = "{'id':'00000000-0000-0000-0000-000000000000','name':'test','templateTypeName':'Очередь','templateIntervals':[{'startTime':'08:00','endTime':'10:00','limit':10}]}".encode('UTF-8')
        self.nostart = "{'name': 'test-0107','templateTypeName':'Очередь','active':true,'templateIntervals':[{'endTime':'14:00','limit':10}]}".encode('UTF-8')
        self.noend = "{'name': 'test-0107','templateTypeName':'Очередь','active':true,'templateIntervals':[{'startTime':'10:00','limit':10}]}".encode('UTF-8')

        self.create_template = "{'name': 'autotest_template','templateTypeName':'Очередь','templateIntervals':[{'dayOfWeekStart':1,'dayOfWeekEnd':3,'startTime':'10:00','endTime':'14:00','limit':10}]}"
        self.update_template = "{'id':'autotest_id','name':'template_name','active':true,'templateTypeName':'Очередь','templateIntervals':[{'startTime':'START','endTime':'END','limit':10}]}"
        self.post_search = "{'name':'автотест','active':true}".encode('UTF-8')
        self.post_search_admin = "{'name':'шаблон','active':true,'orgIds':['4107450a-67a2-e4a4-ac5d-688cb9c3b70f']}".encode('UTF-8')

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

        #без startTime и endTime
        nostart = MyRequests.post('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.nostart)
        Assertions.assert_json_value_by_name(nostart, 'message', 'Не указано время начала приёма','Текст ошибки при отсутствии startTime не равен ожидаемому')

        noend = MyRequests.post('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.noend)
        Assertions.assert_json_value_by_name(noend, 'message', 'Не указано время окончания приёма','Текст ошибки при отсутствии endTime не равен ожидаемому')

    @allure.feature("Передача несуществующего id")
    def test_incorrect_id(self):

        #делаю get
        get = MyRequests.get(f'/tm-schedule/api/templates/{config.fake_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get, 'message', f"Шаблон с id={config.fake_id} не найден", 'Сообщение об ошибке не равно ожидаемому')

        #put
        put = MyRequests.put('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'}, data=self.incorrectid)
        Assertions.assert_json_value_by_name(put, 'message', f"Шаблон с id={config.fake_id} не найден",'Сообщение об ошибке не равно ожидаемому')

        #не передать id при обновлении
        self.update_template = self.update_template.replace('autotest_id','')
        update = MyRequests.put('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'}, data=self.update_template.encode('UTF-8'))
        Assertions.assert_json_value_by_name(update, 'message', f"Идентификатор шаблона не указан",'Сообщение об ошибке не равно ожидаемому')

        #delete
        delete = MyRequests.delete(f'/tm-schedule/api/templates/{config.fake_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', f"Шаблон с id={config.fake_id} не найден",'Сообщение об ошибке не равно ожидаемому')

    @allure.feature("Создание/получение/обновление/удаление шаблона")
    def test_create_get_put_delete(self):

        self.create_template = self.create_template.replace('autotest_template', f'autotest_template {str(datetime.datetime.now())}')

        #создаю шаблон
        create = MyRequests.post('/tm-schedule/api/templates', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                 data=self.create_template.encode('UTF-8'))
        Assertions.assert_json_value_by_name(create, 'success', True, 'Создание шаблона завершилось неуспешно')

        #берем из ответа id шаблона
        template_id = create.json()['result']['id']

        #делаем get запрос по созданному ранее шаблону
        get = MyRequests.get(f'/tm-schedule/api/templates/{template_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, template_id, get.json()['result']['id'],'В ответе get метода нет данных по созданному шаблону')

        replace_values = {'autotest_id': template_id, 'START': '15:55', 'END': '17:34', 'template_name': f'autotest_template_update {str(datetime.datetime.now())}'}
        self.update_template = self.multiple_replace(self.update_template, replace_values)

        #обновляем шаблону описание
        put = MyRequests.put('/tm-schedule/api/templates',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                             data=self.update_template.encode('UTF-8'))
        Assertions.assert_expectedvalue_equal_receivedvalue(put, '15:55', put.json()['result']['templateIntervals'][0]['startTime'],'startTime шаблона при обновлении не обновилось')
        Assertions.assert_expectedvalue_equal_receivedvalue(put, '17:34', put.json()['result']['templateIntervals'][0]['endTime'],'endTime шаблона при обновлении не обновилось')

        #делаю delete запрос
        delete = MyRequests.delete(f'/tm-schedule/api/templates/{template_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление шаблона неуспешно')

        #проверяю делая get
        get_deleted = MyRequests.get(f'/tm-schedule/api/templates/{template_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get_deleted, False, get.json()['result']['active'],'Шаблон остался активен после удаления')

    @allure.feature("Проверка что методы поиска рабочие")
    def test_search_template(self):

        #поиск шаблонов GET
        get_search = MyRequests.get('/tm-schedule/api/templates/search?name=%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82&active=true&pageIndex=1&pageSize=5',
                                    headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get_search, 'Шаблон для автотестов', get_search.json()['result']['items'][0]['name'], 'Полученное название шаблона не равно ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(get_search, 1,get_search.json()['result']['totalSize'],'Найдено больше, чем одно значение')

        #поиск шаблонов POST
        post_search = MyRequests.post('/tm-schedule/api/templates/search', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                      data=self.post_search)
        Assertions.assert_expectedvalue_equal_receivedvalue(post_search, 'Шаблон для автотестов', post_search.json()['result']['items'][0]['name'], 'Полученное название шаблона не равно ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(post_search, 1,post_search.json()['result']['totalSize'],'Найдено больше, чем одно значение')

        #админский поиск шаблонов GET
        get_search_admin = MyRequests.get('/tm-schedule/api/templates/admin/search?name=%D1%88%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD&active=true&orgIds=4107450a-67a2-e4a4-ac5d-688cb9c3b70f&pageIndex=1&pageSize=5',
                                          headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get_search_admin, 'Название шаблона',get_search_admin.json()['result']['items'][0]['name'],'Полученное название шаблона не равно ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(get_search_admin, 1,get_search_admin.json()['result']['totalSize'],'Найдено больше, чем одно значение')

        #админский поиск шаблонов POST
        post_search_admin = MyRequests.post('/tm-schedule/api/templates/admin/search', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                      data=self.post_search_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(post_search_admin, 'Название шаблона', post_search_admin.json()['result']['items'][0]['name'], 'Полученное название шаблона не равно ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(post_search_admin, 1, post_search_admin.json()['result']['totalSize'], 'Найдено больше, чем одно значение')