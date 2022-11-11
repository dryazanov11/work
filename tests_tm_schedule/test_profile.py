import datetime

import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Profile")
class TestProfile(BaseCase):

    def setup(self):
        self.noname = "{'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}"
        self.noattribute = "{'name': 'test','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc'}"

        self.reqattr = "{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceName':'Возрастная категория граждан','route':'$.observation.ageType','required':true,'parameterType':'value'}"
        self.norequiredattribute = "{'name': 'test','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.56','referenceCode':'100'}]}"


        self.notexistlocation = "{'name':'test','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}],'locationIds':['3fa85f64-5717-4562-b3fc-2c963f66afa6']}"
        self.notexistworkflow = "{'name':'test','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}],'workflowId':'3fa85f64-5717-4562-b3fc-2c963f66afa6'}"

        self.put = "{'name': 'test','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}"

        self.request_create_profile = "{'name':'autotest_profile','active':true,'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}],'checkBookingAvailable':false,'locationIds':['11721fff-0a00-410e-93a6-c6f6ce963e5d','43f6b95d-5bda-4290-8a67-f77bc86d78e1'],'createdOrgId':'91593c1f-c130-4312-9a97-8c017de6a1de','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc'}"
        self.request_update_profile = "{'name':'autotest_profile_update','workflowId':'52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc','description':'update profile','profileAttributes':[{'id':'8861c591-e514-4707-8438-cc1fa70ab75e','referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}"
        self.request_profile_search = "{'name':'авто','references':[{'referenceKey':'1.2.643.5.1.13.13.11.1070','values':[{'referenceCode':'B01.064.003'}]}],'pageIndex':1,'pageSize':20}".encode('UTF-8')
        self.available = "{'context':{'profile':{'id':'3bbdc3b9-5506-47bb-933a-821d22960a23'}},'serviceRequest':{'medicalServices':'B01.064.003'}}"
        self.request_profile_admin_search = "{'name':'20','status':true,'workflowIds':['52f2d5c0-3bb5-4ebb-ae4a-2e4a6b4cbcfc'],'pageIndex':1,'pageSize':10,'orgIds':['4107450a-67a2-e4a4-ac5d-688cb9c3b70f']}"
        self.request_profile_unique_attr = "{'target':{'referenceKey':'1.2.643.5.1.13.13.11.1070'},'filter':[{'referenceKey':'1.2.643.5.1.13.13.11.1070','referenceCode':'B01.064.003'}]}"
        self.request_profile_unique_attr_admin = "{'target':{'referenceKey':'1.2.643.2.69.1.1.1.56'},'filter':[{'referenceKey':'1.2.643.2.69.1.1.1.56','referenceCode':'100'}]}"

    @allure.feature("Создание профиля не передавая обязательные параметры")
    def test_create_profile_negative(self):

        #не передаю name
        name = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.noname)
        Assertions.assert_json_value_by_name(name, 'message', 'Название не может быть пустым', 'Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(name, 'errorCode', 4, 'Получен не ожидаемый код ошибки')

        #не передаю profileAttributes
        no_attribute = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data=self.noattribute)
        Assertions.assert_json_value_by_name(no_attribute, 'message','Не указаны атрибуты профиля' ,'Ошибка об отсутствии profileAttributes не корректна')
        Assertions.assert_json_value_by_name(no_attribute, 'errorCode', 4, 'Получен не ожидаемый код ошибки')

        #делаю атрибут обязательным
        required_true = MyRequests.put(f'/tm-schedule/api/systems/config/cb32110f-6678-46ba-a7f7-c8ae9297410a', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data=self.reqattr.encode('UTF-8'))
        Assertions.assert_expectedvalue_equal_receivedvalue(required_true, True, required_true.json()['result']['required'], 'Сделать атрибут обязательным не удалось')

        #не передаю атрибут профиля, который является обязательным
        no_required_attribute = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data=self.norequiredattribute)
        Assertions.assert_json_value_by_name(no_required_attribute, 'message', "Отсутствует обязательный атрибут: '1.2.643.2.69.1.1.1.223'",'Ошибка об отсутствии обязательного атрибута не корректна')
        Assertions.assert_json_value_by_name(no_required_attribute, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #убираю обязательность у атрибута
        self.reqattr = self.reqattr.replace('true','false')

        required_false = MyRequests.put(f'/tm-schedule/api/systems/config/cb32110f-6678-46ba-a7f7-c8ae9297410a', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data=self.reqattr.encode('UTF-8'))
        Assertions.assert_expectedvalue_equal_receivedvalue(required_false, False, required_false.json()['result']['required'], 'Сделать атрибут необязательным не удалось')

        #передаю несуществуюший id location
        not_exist_location = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                             data=self.notexistlocation)
        Assertions.assert_json_value_by_name(not_exist_location, 'message','Не найдены места оказания услуг со следующими id: 3fa85f64-5717-4562-b3fc-2c963f66afa6','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(not_exist_location, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #передаю несуществующий id workflow
        not_exist_workflow = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                             data=self.notexistworkflow)
        Assertions.assert_json_value_by_name(not_exist_workflow, 'message','Маршрут с указанным id=3fa85f64-5717-4562-b3fc-2c963f66afa6 не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(not_exist_workflow, 'errorCode', 11, 'Получен не ожидаемый код ошибки')

    @allure.feature("Передача несуществующего id профиля")
    def test_incorrect_id(self):

        #делаю get запрос
        get = MyRequests.get(f'/tm-schedule/api/profiles/{config.fake_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get, 'message', f'Профиль с id={config.fake_id} не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(get, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #делаю put запрос
        put = MyRequests.put(f'/tm-schedule/api/profiles/{config.fake_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                             data=self.put)
        Assertions.assert_json_value_by_name(put, 'message', 'Профиль с указанным идентификатором не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(put, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #делаю delete запрос
        delete = MyRequests.delete(f'/tm-schedule/api/profiles/{config.fake_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', 'Профиль не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(delete, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

    @allure.feature("Создание/получение/обновление/удаление профиля")
    def test_create_get_put_delete(self):

        self.request_create_profile = self.request_create_profile.replace('autotest_profile', f'autotest_profile {str(datetime.datetime.now())}')

        #создаю профиль
        create = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data=self.request_create_profile)
        Assertions.assert_json_value_by_name(create, 'success', True, 'Создание профиля завершилось неуспешно')

        #берем из ответа id профиля
        profile_id = create.json()['result']['id']

        #делаем get запрос по созданному ранее профилю
        get = MyRequests.get(f'/tm-schedule/api/profiles/{profile_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, profile_id, get.json()['result']['id'], 'В ответе get метода нет данных по созданному профилю')

        self.request_update_profile = self.request_update_profile.replace('autotest_profile_update',f'autotest_profile update {str(datetime.datetime.now())}')

        #обновляем профилю описание
        put = MyRequests.put(f'/tm-schedule/api/profiles/{profile_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                             data=self.request_update_profile)
        Assertions.assert_expectedvalue_equal_receivedvalue(put, 'update profile', put.json()['result']['description'], 'Описание профиля при обновлении не обновилось')
        Assertions.assert_json_value_by_name(put, 'success', True, 'Обновление профиля завершилось неуспешно')

        #делаю delete запрос
        delete = MyRequests.delete(f'/tm-schedule/api/profiles/{profile_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(delete, False, delete.json()['result']['active'], 'В результате удаления профиля его статус остался True')
        Assertions.assert_json_value_by_name(delete, 'success', True,'Удаление профиля неуспешно')

    @allure.feature("Проверка что методы поиска рабочие")
    def test_search_profile(self):

        #получение списка профилей
        search = MyRequests.post('/tm-schedule/api/profiles/search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data=self.request_profile_search)
        Assertions.assert_expectedvalue_equal_receivedvalue(search, 'd0e0a86c-4442-438d-895a-8e6fd1718c45', search.json()['result']['items'][0]['id'], 'Полученный профиль отличается от ожидаемого')
        Assertions.assert_expectedvalue_equal_receivedvalue(search, 1, search.json()['result']['totalSize'], 'Найдено больше, чем одно значение')

        #проверка возможности использовать профиль обслуживания для TMCore
        available = MyRequests.post('/tm-schedule/api/profiles/available', headers={'Content-Type': 'application/json-patch+json'}, data=self.available)
        Assertions.assert_json_value_by_name(available, 'success', True, 'Проверка возможности использовать профиль неуспешна')

        #админский поиск профиля из другой МО
        admin_search = MyRequests.post('/tm-schedule/api/profiles/admin/search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data=self.request_profile_admin_search)
        Assertions.assert_expectedvalue_equal_receivedvalue(admin_search, 'd82021bd-cb94-431f-85ec-c0fb54b642e9', admin_search.json()['result']['items'][0]['id'],
                                                            'Полученный профиль отличается от ожидаемого')
        Assertions.assert_expectedvalue_equal_receivedvalue(admin_search, 1, admin_search.json()['result']['totalSize'], 'Найдено больше, чем одно значение')

        #поиск уникальный атрибутов профиля по заданным параметрам
        unique_attr = MyRequests.post('/tm-schedule/api/profiles/uniqueAttributes',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data=self.request_profile_unique_attr)
        Assertions.assert_expectedvalue_equal_receivedvalue(unique_attr, 'Прием (осмотр, консультация) врача-стоматолога детского первичный',unique_attr.json()['result'][0]['referenceName'],
                                                            'Полученный атрибут отличается от ожидаемого')

        #поиск уникальных атрибутов админский
        unique_attr_admin = MyRequests.post('/tm-schedule/api/profiles/admin/uniqueAttributes', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                            data=self.request_profile_unique_attr_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(unique_attr_admin,'Колопроктология',unique_attr_admin.json()['result'][0]['referenceName'],
                                                            'Полученный атрибут отличается от ожидаемого')

