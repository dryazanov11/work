import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Location")
class TestLocation(BaseCase):

    def setup(self):
        self.noname = "{'physicalType':'ro','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de','partOf':'11721fff-0a00-410e-93a6-c6f6ce963e5d'}"
        self.noaddress = "{'name':'test','physicalType':'bu','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de'}"
        self.nophysicaltype = "{'name':'test','address':'test','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de'}"
        self.nopartof = "{'name':'test','physicalType':'ro','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de'}"
        self.nocontacttype = "{'name':'test','address':'test','physicalType':'bu','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de','telecom':[{'value':'string'}]}"
        self.novalue = "{'name':'test','address':'test','physicalType':'bu','managingOrganization':'91593c1f-c130-4312-9a97-8c017de6a1de','telecom':[{'contactType':'string'}]}"

        self.create_location_bu = "{'name':'name_autotest','address':'address_autotest','physicalType':'bu'}"
        self.create_location_ro = "{'name':'name_autotest','address':'address_autotest','physicalType':'ro','partOf':'part_of_building'}"
        self.request_search_location = "{'name':'Первое здание (для автотестов)','active':true,'address':'ул. Пушкина, д. Колотушкина','physicalType':['bu'],'pageIndex':1,'pageSize':10}".encode('UTF-8')
        self.request_search_location_admin = "{'name':'Кабинет функциональной диагностики для автотеста','active':true,'physicalType':['ro'],'partOf':['34d26711-4c81-4b8e-9f93-787adbe644b7'],'pageIndex':1,'pageSize':10,'managingOrganizations':['0b09d9d0-3137-472d-bc1e-bdf2cc9730ce']}".encode('UTF-8')

    @allure.feature("Создание локации не передавая обязательные параметры")
    def test_create_location_negative(self):
        #без name - 0..1 (0..1 для зданий 1..1 для кабинетов)
        name = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.noname)
        Assertions.assert_json_value_by_name(name, 'message', 'Название кабинета не может быть пустым', 'Ошибка при отсутствии name в запросе создания кабинета не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(name, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

        #без address - 0..1 (1..1 для зданий 0..1 для кабинетов)
        address = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.noaddress)
        Assertions.assert_json_value_by_name(address, 'message', 'Не указан адрес', 'Ошибка при отсутствии address в запросе создания здания не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(address, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

        #без physicalType - 1..1 "ro" | "bu"
        physicalType = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.nophysicaltype)
        Assertions.assert_json_value_by_name(physicalType, 'message', "Не указан тип места оказания услуг ('ro' - для кабинета, 'bu' - для здания)", 'Ошибка при отсутствии physicalType в запросе не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(physicalType, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

        #без partOf - 0..1 (0..1 для зданий 1..1 для кабинетов)
        partof = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.nopartof)
        Assertions.assert_json_value_by_name(partof, 'message', "Не указан 'partOf' (идентификатор строения)", 'Ошибка при отсутствии partOf в запросе создания кабинета не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(partof, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

        #без telecom - 0..* - 1..1 для system и 1..1 для value
        telecom_contacttype = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.nocontacttype)
        Assertions.assert_json_value_by_name(telecom_contacttype, 'message', "Тип контакта не может быть пустым",'Ошибка при отсутствии contactType в запросе не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(telecom_contacttype, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

        telecom_value = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.novalue)
        Assertions.assert_json_value_by_name(telecom_value, 'message', "Значение контакта не может быть пустым",'Ошибка при отсутствии value в запросе не соответствует ожидаемому значению')
        Assertions.assert_json_value_by_name(telecom_value, 'errorCode', 4, 'Значение errorCode не соответсвует ожидаемому')

    @allure.feature("Проверка несуществующего id локации")
    def test_incorrect_id(self):

        #делаем get запрос
        get = MyRequests.get(f'/tm-schedule/api/location/{config.fake_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get, 'message', f'Место оказания медицинских услуг с id={config.fake_id} не найдено', 'Ожидаемая ошибка не получена')
        Assertions.assert_json_value_by_name(get, 'errorCode', 19, 'Значение errorCode не соответсвует ожидаемому')

        #делаем put запрос
        put = MyRequests.put(f'/tm-schedule/api/location/{config.fake_id}',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                             data=self.create_location_bu)
        Assertions.assert_json_value_by_name(put, 'message',f'Место оказания услуг не найдено для id={config.fake_id}','Ожидаемая ошибка не получена')
        Assertions.assert_json_value_by_name(put, 'errorCode', 19,'Значение errorCode не соответсвует ожидаемому')

        #делаем delete запрос
        delete = MyRequests.delete(f'/tm-schedule/api/location/{config.fake_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', f'Место оказания услуг не найдено для id={config.fake_id}', 'Ожидаемая ошибка не получена')
        Assertions.assert_json_value_by_name(delete, 'errorCode', 19, 'Значение errorCode не соответсвует ожидаемому')

    @allure.feature("Создание/получение/обновление/удаление локации")
    def test_create_get_put_delete_location(self):

        #создаем здание
        building = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},data=self.create_location_bu)
        Assertions.assert_expectedvalue_equal_receivedvalue(building, True, building.json()['result']['active'], 'Создание здания прошло неуспешно')
        Assertions.assert_json_value_by_name(building, 'errorCode', 0, 'Значение errorCode не соответсвует ожидаемому')

        #вытаскиваем из ответа id
        building_id = building.json()['result']['id']

        #делаем get запрос
        building_get = MyRequests.get(f'/tm-schedule/api/location/{building_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(building_get, building_id, building_get.json()['result']['id'], 'Метод get отработал неуспешно')
        Assertions.assert_json_value_by_name(building_get, 'errorCode', 0, 'Значение errorCode не соответсвует ожидаемому')

        #делаем put запрос
        replace_values = {'name_autotest': 'name_autotest_update', 'address_autotest': 'address_autotest_update'}
        self.create_location_bu = self.multiple_replace(self.create_location_bu, replace_values)
        building_put = MyRequests.put(f'/tm-schedule/api/location/{building_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                      data=self.create_location_bu)
        Assertions.assert_expectedvalue_equal_receivedvalue(building_put, 'name_autotest_update', building_put.json()['result']['name'],'Обновление name прошло неуспешно')
        Assertions.assert_expectedvalue_equal_receivedvalue(building_put, 'address_autotest_update',building_put.json()['result']['address'],'Обновление address прошло неуспешно')
        Assertions.assert_json_value_by_name(building_put, 'errorCode', 0, 'Значение errorCode не соответсвует ожидаемому')

        #заменяем в запросе из конфига partOf на полученный ранее id
        self.create_location_ro = self.create_location_ro.replace('part_of_building', f'{building_id}')

        #создаем в этом здании кабинет
        cabinet = MyRequests.post('/tm-schedule/api/location', headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_schedule}'},
                                   data=self.create_location_ro)

        Assertions.assert_expectedvalue_equal_receivedvalue(cabinet, True, cabinet.json()['result']['active'],'Создание кабинета прошло неуспешно')
        Assertions.assert_json_value_by_name(cabinet, 'errorCode', 0, 'Значение errorCode не соответсвует ожидаемому')

        #вытаскиваем из ответа id
        cabinet_id = cabinet.json()['result']['id']

        #удаляем здание и кабинет
        del_bu = MyRequests.delete(f'/tm-schedule/api/location/{building_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        del_ro = MyRequests.delete(f'/tm-schedule/api/location/{cabinet_id}', headers={'Authorization': f'{config.token_test_schedule}'})

    @allure.feature("Проверка что методы поиска рабочие")
    def test_search_locations(self):

        #ищу локацию в рамках МО от токена
        search_post = MyRequests.post('/tm-schedule/api/location/_search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                   data=self.request_search_location)
        Assertions.assert_expectedvalue_equal_receivedvalue(search_post, '11721fff-0a00-410e-93a6-c6f6ce963e5d', search_post.json()['result']['items'][0]['id'],'POST поиск прошел неуспешно')
        Assertions.assert_expectedvalue_equal_receivedvalue(search_post, 1, search_post.json()['result']['totalSize'], 'Количество локаций не соответсвует ожидаемому')

        search_get = MyRequests.get('/tm-schedule/api/location/_search?name=%D0%9F%D0%B5%D1%80%D0%B2%D0%BE%D0%B5%20%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%28%D0%B4%D0%BB%D1%8F%20%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D0%BE%D0%B2%29&active=true&address=%D1%83%D0%BB.%20%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D0%B0%2C%20%D0%B4.%20%D0%9A%D0%BE%D0%BB%D0%BE%D1%82%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D0%B0&physicalType=bu&pageIndex=1&pageSize=10',
                                    headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(search_get, '11721fff-0a00-410e-93a6-c6f6ce963e5d',search_get.json()['result']['items'][0]['id'],'GET поиск прошел неуспешно')
        Assertions.assert_expectedvalue_equal_receivedvalue(search_get, 1, search_get.json()['result']['totalSize'], 'Количество локаций не соответсвует ожидаемому')

        #ищу локацию в другой МО
        search_post_admin = MyRequests.post('/tm-schedule/api/admin/location/_search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                   data=self.request_search_location_admin)
        Assertions.assert_expectedvalue_equal_receivedvalue(search_post_admin, '98c8620a-2451-4296-9355-f59dbb8e4486', search_post_admin.json()['result']['items'][0]['id'], 'Админский POST поиск прошел неуспешно')
        Assertions.assert_expectedvalue_equal_receivedvalue(search_post_admin, 1, search_post_admin.json()['result']['totalSize'], 'Количество локаций не соответсвует ожидаемому')

        search_get_admin = MyRequests.get('/tm-schedule/api/admin/location/_search?name=%D0%9A%D0%B0%D0%B1%D0%B8%D0%BD%D0%B5%D1%82%20%D1%84%D1%83%D0%BD%D0%BA%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D0%B4%D0%B8%D0%B0%D0%B3%D0%BD%D0%BE%D1%81%D1%82%D0%B8%D0%BA%D0%B8%20%D0%B4%D0%BB%D1%8F%20%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D0%B0&active=true&managingOrganizations=0b09d9d0-3137-472d-bc1e-bdf2cc9730ce&partOf=34d26711-4c81-4b8e-9f93-787adbe644b7&physicalType=ro&pageIndex=1&pageSize=100',
                                          headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(search_get_admin, '98c8620a-2451-4296-9355-f59dbb8e4486',search_get_admin.json()['result']['items'][0]['id'],'GET поиск прошел неуспешно')
        Assertions.assert_expectedvalue_equal_receivedvalue(search_get_admin, 1, search_get_admin.json()['result']['totalSize'], 'Количество локаций не соответсвует ожидаемому')