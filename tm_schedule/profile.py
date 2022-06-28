import datetime

import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Profile")
class TestProfile(BaseCase):

    @allure.feature("Создание профиля не передавая обязательные параметры")
    def test_create_profile_negative(self):

        #не передаю name
        name = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data="{'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}")
        Assertions.assert_json_value_by_name(name, 'message', 'Название не может быть пустым', 'Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(name, 'errorCode', 4, 'Получен не ожидаемый код ошибки')

        #не передаю profileAttributes
        no_attribute = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},data="{'name': 'test'}")
        Assertions.assert_json_value_by_name(no_attribute, 'message','Не указаны атрибуты профиля' ,'Ошибка об отсутствии profileAttributes не корректна')
        Assertions.assert_json_value_by_name(no_attribute, 'errorCode', 4, 'Получен не ожидаемый код ошибки')

        #передаю уже существующее название профиля
        exist_name = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                               data="{'name': 'Первый профиль для автотестов', 'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}".encode('UTF-8'))
        Assertions.assert_json_value_by_name(exist_name, 'message', 'Название не уникально для текущей организации','Ошибка о дубле названия не корректна')
        Assertions.assert_json_value_by_name(exist_name, 'errorCode', 18, 'Получен не ожидаемый код ошибки')

        #не передаю атрибут профиля, который является обязательным
        no_required_attribute = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data="{'name': 'test', 'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.56','referenceCode':'100'}]}")
        Assertions.assert_json_value_by_name(no_required_attribute, 'message', "Отсутствует обязательный атрибут: '1.2.643.2.69.1.1.1.223'",'Ошибка об отсутствии обязательного атрибута не корректна')
        Assertions.assert_json_value_by_name(no_required_attribute, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #передаю несуществуюший id location
        not_exist_location = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                             data="{'name':'test','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}],'locationIds':['3fa85f64-5717-4562-b3fc-2c963f66afa6']}")
        Assertions.assert_json_value_by_name(not_exist_location, 'message','Не найдены места оказания услуг со следующими id: 3fa85f64-5717-4562-b3fc-2c963f66afa6','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(not_exist_location, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #передаю несуществующий id workflow
        not_exist_workflow = MyRequests.post('/tm-schedule/api/profiles',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                             data="{'name':'test','profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}],'workflowId':'3fa85f64-5717-4562-b3fc-2c963f66afa6'}")
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
                             data="{'name': 'test', 'profileAttributes':[{'referenceKey':'1.2.643.2.69.1.1.1.223','referenceCode':'4'}]}")
        Assertions.assert_json_value_by_name(put, 'message', 'Профиль с указанным идентификатором не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(put, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

        #делаю delete запрос
        delete = MyRequests.delete(f'/tm-schedule/api/profiles/{config.fake_id}',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', 'Профиль не найден','Ошибка об отсутствии названия не корректна')
        Assertions.assert_json_value_by_name(delete, 'errorCode', 19, 'Получен не ожидаемый код ошибки')

    @allure.feature("Создание/получение/обновление/удаление профиля")
    def test_create_get_put_delete(self):

        config.request_create_profile = config.request_create_profile.replace('autotest_profile', f'autotest_profile {str(datetime.datetime.now())}')

        #создаю профиль
        create = MyRequests.post('/tm-schedule/api/profiles', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data=config.request_create_profile)
        Assertions.assert_json_value_by_name(create, 'success', True, 'Создание профиля завершилось неуспешно')

        #берем из ответа id профиля
        profile_id = create.json()['result']['id']

        #делаем get запрос по созданному ранее профилю
        get = MyRequests.get(f'/tm-schedule/api/profiles/{profile_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get, profile_id, get.json()['result']['id'], 'В ответе get метода нет данных по созданному профилю')

        config.request_update_profile = config.request_update_profile.replace('autotest_profile_update',f'autotest_profile update {str(datetime.datetime.now())}')

        #обновляем профилю описание
        put = MyRequests.put(f'/tm-schedule/api/profiles/{profile_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                             data=config.request_update_profile)
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
                                 data=config.request_profile_search.encode('UTF-8'))
        Assertions.assert_expectedvalue_equal_receivedvalue(search, 'd0e0a86c-4442-438d-895a-8e6fd1718c45', search.json()['result']['items'][0]['id'], 'Полученный профиль отличается от ожидаемого')

        #проверка возможности использовать профиль обслуживания для TMCore
        available = MyRequests.post('/tm-schedule/api/profiles/available', headers={'Content-Type': 'application/json-patch+json'},
                                    data="{'context':{'profile':{'id':'d82021bd-cb94-431f-85ec-c0fb54b642e9'}},'serviceRequest':{'category':'100'}}")
        Assertions.assert_json_value_by_name(available, 'success', True, 'Проверка возможности использовать профиль неуспешна')

        #админский поиск профиля из другой МО
        admin_search = MyRequests.post('/tm-schedule/api/profiles/admin/search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data=config.request_profile_admin_search)
        Assertions.assert_expectedvalue_equal_receivedvalue(admin_search, 'd82021bd-cb94-431f-85ec-c0fb54b642e9', admin_search.json()['result']['items'][0]['id'],
                                                            'Полученный профиль отличается от ожидаемого')

        #поиск уникальный атрибутов профиля по заданным параметрам
        unique_attr = MyRequests.post('/tm-schedule/api/profiles/uniqueAttributes',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                       data=config.request_profile_unique_attr)
        Assertions.assert_expectedvalue_equal_receivedvalue(unique_attr, 'Прием (осмотр, консультация) врача-стоматолога детского первичный',unique_attr.json()['result'][0]['referenceName'],
                                                            'Полученный атрибут отличается от ожидаемого')

        #поиск уникальных атрибутов админский
        unique_attr_admin = MyRequests.post('/tm-schedule/api/profiles/admin/uniqueAttributes', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                            data=config.request_profile_unique_attr_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(unique_attr_admin,'Колопроктология',unique_attr_admin.json()['result'][0]['referenceName'],
                                                            'Полученный атрибут отличается от ожидаемого')

