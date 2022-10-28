import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Practitioner")
class TestPractitioner(BaseCase):

    def setup(self):
        self.create = "{'snils':'01069948355'}"
        self.createinvalid = "{'snils':'40765449391'}"

        self.create_admin = "{'snils':'57585823657','organizationId':'dfe3eec2-8a79-4921-9b58-0ce03a5e6c10'}"
        self.createinvalid_admin = "{'snils':'57585823651','organizationId':'dfe3eec2-8a79-4921-9b58-0ce03a5e6c10'}"
        self.createinvalidmo_admin = "{'snils':'57585823657','organizationId':'dfe3eec2-8a79-4921-9b58-0ce03a5e6c11'}"
        self.nosnils_admin = "{'organizationId':'dfe3eec2-8a79-4921-9b58-0ce03a5e6c11'}"
        self.nomo_admin = "{'snils':'57585823657'}"

        self.request_search = "{'snils':['01069948355'],'pageSize':10,'pageIndex':1,'active':true}"
        self.request_search_admin = "{'snils':['57585823657'],'postName':'врач-нейрохирург','specialityName':'Неврология','pageSize':10,'pageIndex':1,'active':true,'orgIds':['dfe3eec2-8a79-4921-9b58-0ce03a5e6c10']}".encode('UTF-8')

    @allure.feature("Создание записи о специалисте")
    def test_create_practitioner(self):

        #создание записи о специалисте
        create = MyRequests.post('/tm-schedule/api/practitioner/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                 data=self.create)
        Assertions.assert_expectedvalue_equal_receivedvalue(create, config.practitioner_id, create.json()['result']['id'], 'Полученный id врача не равен ожидаемому')
        Assertions.assert_json_value_by_name(create, 'success', True, 'Получен неуспешный статус')

        #создание с несуществующим снилс
        create_invalid = MyRequests.post('/tm-schedule/api/practitioner/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                 data=self.createinvalid)
        Assertions.assert_json_value_by_name(create_invalid, 'message', 'Метод terminologyClient.GetDoctorInfo вернул пустое значение', 'Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_invalid, 'success', False, 'Получен успешный статус')

        #вообще не передать параметр снилс
        create_empty = MyRequests.post('/tm-schedule/api/practitioner/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                         data="{}")
        Assertions.assert_json_value_by_name(create_empty, 'message',"Value cannot be null. (Parameter 'doctorSnils')",'Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_empty, 'success', False, 'Получен успешный статус')

    @allure.feature("Создание админской записи о специалисте")
    def test_admin_create_practitioner(self):

        #создание записи о специалисте в МО из запроса
        create = MyRequests.post('/tm-schedule/api/practitioner/admin/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                 data=self.create_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(create, '7f215850-e51c-4996-a6d9-6905fc2408b0',create.json()['result']['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_json_value_by_name(create, 'success', True, 'Получен неуспешный статус')

        #передать неверный снилс
        create_invalid_snils = MyRequests.post('/tm-schedule/api/practitioner/admin/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                         data=self.createinvalid_admin)
        Assertions.assert_json_value_by_name(create_invalid_snils, 'message','Метод terminologyClient.GetDoctorInfo вернул пустое значение','Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_invalid_snils, 'success', False, 'Получен успешный статус')

        #передать неверный код МО
        create_invalid_mo = MyRequests.post('/tm-schedule/api/practitioner/admin/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                               data=self.createinvalidmo_admin)
        Assertions.assert_json_value_by_name(create_invalid_mo, 'message','Не удалось найти информацию об организации dfe3eec2-8a79-4921-9b58-0ce03a5e6c11','Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_invalid_mo, 'success', False, 'Получен успешный статус')

        #не передать снилс
        create_empty_snils = MyRequests.post('/tm-schedule/api/practitioner/admin/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                       data=self.nosnils_admin)
        Assertions.assert_json_value_by_name(create_empty_snils, 'message', "Value cannot be null. (Parameter 'doctorSnils')",'Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_empty_snils, 'success', False, 'Получен успешный статус')

        #не передать МО
        create_empty_mo = MyRequests.post('/tm-schedule/api/practitioner/admin/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                             data=self.nomo_admin)
        Assertions.assert_json_value_by_name(create_empty_mo, 'message',"Не найдено ни одной подходящей записи среди списка должностей",'Получено неожидаемое сообщение об ошибке')
        Assertions.assert_json_value_by_name(create_empty_mo, 'success', False, 'Получен успешный статус')

    @allure.feature("Проверка общих методов поиска специалиста")
    def test_search_practitioner(self):

        #ищем специалиста
        search = MyRequests.post('/tm-schedule/api/practitioner/search', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                 data=self.request_search)
        Assertions.assert_expectedvalue_equal_receivedvalue(search, config.practitioner_id,search.json()['result']['items'][0]['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(search, 1, search.json()['result']['totalSize'], 'Количество врачей не равно ожидаемому')
        Assertions.assert_json_value_by_name(search, 'success', True, 'Получен неуспешный статус')

        #ищем специалиста в другой МО
        search_admin = MyRequests.post('/tm-schedule/api/practitioner/admin/search',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                 data=self.request_search_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(search_admin, '7f215850-e51c-4996-a6d9-6905fc2408b0',search_admin.json()['result']['items'][0]['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(search_admin, 1, search_admin.json()['result']['totalSize'],'Количество врачей не равно ожидаемому')
        Assertions.assert_json_value_by_name(search_admin, 'success', True, 'Получен неуспешный статус')

    @allure.feature("Проверка получения данных специалиста и удаления")
    def test_get_delete_practitioner(self):

        #ищем информацию о специалисте по его id
        byid = MyRequests.get(f'/tm-schedule/api/practitioner/byId/{config.practitioner_id}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(byid, config.practitioner_id,byid.json()['result']['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_json_value_by_name(byid, 'success', True, 'Получен неуспешный статус')

        #передаем несуществующий id
        byid_invalid = MyRequests.get('/tm-schedule/api/practitioner/byId/a9710575-0095-4f97-a4f6-b32409966101',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(byid_invalid, 'message', 'Специалист с id=a9710575-0095-4f97-a4f6-b32409966101 не найден', 'Полученная ошибка отличается от ожидаемой')
        Assertions.assert_json_value_by_name(byid_invalid, 'success', False, 'Получен успешный статус')

        #ищем информацию о специалисте по его снилс
        bysnils = MyRequests.get(f'/tm-schedule/api/practitioner/bySnils/{config.snils}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(bysnils, config.practitioner_id,bysnils.json()['result']['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_json_value_by_name(bysnils, 'success', True, 'Получен неуспешный статус')

        #передаем несуществующий снилс
        bysnils_invalid = MyRequests.get('/tm-schedule/api/practitioner/bySnils/40765449391',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(bysnils_invalid, 'message','Специалист со СНИЛСом 40765449391 не найден','Полученная ошибка отличается от ожидаемой')
        Assertions.assert_json_value_by_name(bysnils_invalid, 'success', False, 'Получен успешный статус')

        #удаляем врача
        delete = MyRequests.delete(f'/tm-schedule/api/practitioner/delete/{config.practitioner_id}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление прошло неуспешно')

        #удаляем врача с несуществующим id
        delete_invalid = MyRequests.delete('/tm-schedule/api/practitioner/delete/a9710575-0095-4f97-a4f6-b32409966111',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(delete_invalid, 'success', False, 'Удаление прошло успешно')

        #обратно оживляю врача чтобы был доступен в активном статусе
        create = MyRequests.post('/tm-schedule/api/practitioner/create',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                 data=self.create)
        Assertions.assert_expectedvalue_equal_receivedvalue(create, config.practitioner_id,create.json()['result']['id'],'Полученный id врача не равен ожидаемому')
        Assertions.assert_json_value_by_name(create, 'success', True, 'Получен неуспешный статус')
