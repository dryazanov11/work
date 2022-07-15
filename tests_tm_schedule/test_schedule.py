import datetime
from datetime import date
import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
import allure

@allure.epic("Полноценные проверки Schedule")
class TestSchedule(BaseCase):

    def setup(self):
        self.noprofile = "{'startTime':'2022-06-28T10:50:37.565Z','endTime':'2032-06-28T16:50:37.565Z','templateId':'0b97ef57-736b-476d-ba60-8384153c6299','active':true}"
        self.invalidprofile = "{'profileIds':['00000000-0000-0000-0000-000000000000'],'startTime':'2022-06-28T10:50:37.565Z','endTime':'2032-06-28T16:50:37.565Z','templateId':'0b97ef57-736b-476d-ba60-8384153c6299','active':true}"
        self.nostart = "{'profileIds':['5567b7f4-3d0c-4cdb-9bdc-4a9d3273347e'],'endTime':'2032-06-28T16:50:37.565Z','templateId':'0b97ef57-736b-476d-ba60-8384153c6299','active':true}"
        self.noend = "{'profileIds':['5567b7f4-3d0c-4cdb-9bdc-4a9d3273347e'],'startTime':'2022-06-28T16:50:37.565Z','templateId':'0b97ef57-736b-476d-ba60-8384153c6299','active':true}"
        self.notemplate = "{'profileIds':['5567b7f4-3d0c-4cdb-9bdc-4a9d3273347e'],'startTime':'2022-06-28T10:50:37.565Z','endTime':'2032-06-28T16:50:37.565Z','active':true}"
        self.invalidtemplate = "{'profileIds':['5567b7f4-3d0c-4cdb-9bdc-4a9d3273347e'],'startTime':'2022-06-28T10:50:37.565Z','endTime':'2032-06-28T16:50:37.565Z','templateId':'00000000-0000-0000-0000-000000000000','active':true}"

        self.incorrectcell = "{'contextType':'string','context':'string'}"

        self.create_schedule = "{'profileIds':['9a8d83b5-f5fc-4e68-9443-bbdaf23b30bc'],'startTime':'date_from','endTime':'date_to','templateId':'396a8ac8-f668-4c87-abd4-1dbf6522b575','active':true,'owners':[{'externalIdType':'SNILS','externalId':'40765449394'}]}"
        self.update_schedule = "{'profileIds':['9a8d83b5-f5fc-4e68-9443-bbdaf23b30bc'],'active':true,'owners':[{'externalIdType':'SNILS','externalId':'88960841382'}]}"
        self.search_cells = "{'onlyBookingAvailable':true,'startTime':'date_from','endTime':'date_to','scheduleIds':['schedule_id'],'pageIndex':1,'pageSize':10,'withPractitionerOnly':true}"
        self.take_cell = "{'contextType':'type_autotest','context':'context_autotest','actors':[{'externalIdType':'snils','externalId':'04391171038','name':'practitioner_test_name'}]}"

        self.singleevent = "{'profileIds':['9a8d83b5-f5fc-4e68-9443-bbdaf23b30bc'],'startTime':'date_from','endTime':'date_to','templateId':'396a8ac8-f668-4c87-abd4-1dbf6522b575','active':true,'limit':1}"

        self.search_schedule = "{'active':true,'profileIds':['9a8d83b5-f5fc-4e68-9443-bbdaf23b30bc'],'ids':['4a02a1c9-0318-4ba4-8a04-a219ec9703cd'],'pageIndex':1,'pageSize':10}"
        self.search_admin_schedule = "{'profileIds':['97fe1a10-23cc-4eec-afec-bf9f80e5d932'],'active':true,'pageIndex':1,'pageSize':5,'orgIds':['0b09d9d0-3137-472d-bc1e-bdf2cc9730ce']}"
        self.search_admin_cells = "{'startTime':'2022-07-05','endTime':'2022-08-05','pageIndex':1,'pageSize':10,'orgIds':['0b09d9d0-3137-472d-bc1e-bdf2cc9730ce']}"

    @allure.feature('Создание расписания не передавая обязательные параметры')
    def test_create_negative_schedule(self):

        #не передаю профиль
        noprofile = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.noprofile)
        Assertions.assert_json_value_by_name(noprofile, 'message', 'Профили не указаны', 'Неожиданная ошибка при отсутствии профиля')

        #передаю несуществующий профиль
        invalidprofile = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.invalidprofile)
        Assertions.assert_json_value_by_name(invalidprofile, 'message', f'Профиль с id={config.fake_id} не найден', 'Неожиданная ошибка при неверном профиле')

        #не передаю starttime и endtime
        nostart = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.nostart)
        Assertions.assert_json_value_by_name(nostart, 'message', 'Дата начала не указана', 'Неожиданная ошибка об отсутствии starttime')

        noend = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.noend)
        Assertions.assert_json_value_by_name(noend, 'message', 'Дата окончания не указана', 'Неожиданная ошибка об отсутствии endttime')

        #не передаю шаблон
        notemplate = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.notemplate)
        Assertions.assert_json_value_by_name(notemplate, 'message', 'Идентификатор шаблона расписания не указан', 'Неожиданная ошибка об отсутствии шаблона')

        #передаю несуществующий шаблон
        invalidtemplate = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                    data=self.invalidtemplate)
        Assertions.assert_json_value_by_name(invalidtemplate, 'message', f"Шаблон расписания с id={config.fake_id} не найден", 'Неожиданная ошибка при неверном шаблоне')

    @allure.feature('Проверка передачи некорректного id')
    def test_incorrect_id(self):

        #получение расписания по id
        get = MyRequests.get(f'/tm-schedule/api/schedules/{config.default_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(get, 'message', f'Расписание с id={config.default_id} не найдено', 'Некорректная ошибка о несуществующем id расписания')

        #удаление расписания
        delete = MyRequests.delete(f'/tm-schedule/api/schedules/{config.default_id}', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(delete, 'message', f'Расписание с id={config.default_id} не найдено', 'Некорректная ошибка о несуществующем id расписания')

        #обновление расписания
        patch = MyRequests.patch(f'/tm-schedule/api/schedules/update/{config.default_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                                 data="{}")
        Assertions.assert_json_value_by_name(patch, 'message', f'Расписание с id={config.default_id} не найдено', 'Некорректная ошибка о несуществующем id расписания')

        #занятие ячейки с несуществующим id
        take_cell = MyRequests.post(f'/tm-schedule/api/schedules/cell/{config.default_id}/take', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_schedule}'},
                               data=self.incorrectcell)
        Assertions.assert_json_value_by_name(take_cell, 'message' ,f'Ячейка расписания с id={config.default_id} не найдена', 'Некорректная ошибка о несуществующем id ячейки')

        #отмена занятия ячейки с несуществующим id
        cancel_cell = MyRequests.get(f'/tm-schedule/api/schedules/cell/{config.default_id}/cancel', headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(cancel_cell, 'message' ,f'Запись на ячейку с id={config.default_id} не найдена', 'Некорректная ошибка о несуществующей id записи на ячейку')

        #получение справки по занятому месту с несуществующим id
        info_cell = MyRequests.get(f'/tm-schedule/api/schedules/cell/{config.default_id}/info',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(info_cell, 'message',f'Запись на прием с id={config.default_id} не найдена','Некорректная ошибка о несуществующей id записи на прием')

        #изменение статуса оповещения с несуществующим id
        set_cell = MyRequests.get(f'/tm-schedule/api/schedules/actors/{config.default_id}/setVisitStatus',headers={'Authorization': f'{config.token_test_schedule}'})
        Assertions.assert_json_value_by_name(set_cell, 'message',f"Участник с идентификатором {config.default_id} не найден (Parameter 'id')\n",'Некорректная ошибка о несуществующей id записи участника')

        #попытаться занять ячейку, в которой уже нет места
        take_cell = MyRequests.post('/tm-schedule/api/schedules/cell/c13fe5cd-4f5b-401d-9dbb-dc59673724c9/take',headers={'Content-Type': 'application/json-patch+json','Authorization': f'{config.token_test_practitioner}'},
                                    data=self.take_cell)
        Assertions.assert_json_value_by_name(take_cell, 'message', 'Ячейка уже заполнена', 'Ожидаемая ошибка о превышении лимита на ячейку не получена')

    @allure.feature("Создание/получение/обновление/удаление расписания и ячеек")
    def test_create_get_patch_delete(self):

        #в запрос на создание расписание ставлю диапазон в ближайшие 20 дней
        replace_values_schedule = {'date_from': str(date.today()), 'date_to': str(date.today() + datetime.timedelta(days=20))}
        self.create_schedule = self.multiple_replace(self.create_schedule, replace_values_schedule)

        #создание расписания с owners
        create_schedule = MyRequests.post('/tm-schedule/api/schedules/create', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                          data=self.create_schedule)
        Assertions.assert_json_value_by_name(create_schedule, 'success', True, 'Создание расписания завершилось неуспешно')

        schedule_id = create_schedule.json()['result']['id']

        #получение расписания по id
        get_schedule = MyRequests.get(f'/tm-schedule/api/schedules/{schedule_id}',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get_schedule, schedule_id, get_schedule.json()['result']['id'], 'Полученное расписание отличается от ожидаемого')

        #обновить в расписании врача
        update_schedule = MyRequests.patch(f'/tm-schedule/api/schedules/update/{schedule_id}', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                          data=self.update_schedule)
        Assertions.assert_expectedvalue_equal_receivedvalue(update_schedule, '88960841382', update_schedule.json()['result']['owners'][0]['externalId'], 'Полученный СНИЛС врача не равен ожидаемому')
        Assertions.assert_expectedvalue_equal_receivedvalue(update_schedule, 'a528e70e-2864-4803-9f5c-61d17672df42', update_schedule.json()['result']['owners'][0]['practitionerRoleId'], 'Полученный id роли врача не равен ожидаемому')

        #в запрос на поиск ячеек расписания ставлю диапазон в ближайшие 10 дней
        replace_values_cells = {'date_from': str(date.today()), 'date_to': str(date.today() + datetime.timedelta(days=20)), 'schedule_id': schedule_id}
        self.search_cells = self.multiple_replace(self.search_cells, replace_values_cells)

        #делаю запрос на поиск ячеек
        search_cells = MyRequests.post('/tm-schedule/api/schedules/cells', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                       data=self.search_cells)
        Assertions.assert_expectedvalue_equal_receivedvalue(search_cells, schedule_id, search_cells.json()['result']['items'][0]['scheduleId'], 'Расписание ячейки не соответствует ожидаемому')

        schedulecell_id = search_cells.json()['result']['items'][0]['id']

        #записываюсь на доступную ячейку
        take_cell = MyRequests.post(f'/tm-schedule/api/schedules/cell/{schedulecell_id}/take', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                    data=self.take_cell)
        Assertions.assert_json_value_by_name(take_cell, 'success', True, 'Запись на ячейку неуспешна')

        bookedcell_id = take_cell.json()['result']['id']

        #проверить что запись активна
        info_cell = MyRequests.get(f'/tm-schedule/api/schedules/cell/{bookedcell_id}/info', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(info_cell, True, info_cell.json()['result']['active'], 'Полученный статус не активен')
        Assertions.assert_expectedvalue_equal_receivedvalue(info_cell, None, info_cell.json()['result']['actors'][0]['visitStatus'], 'visitStatus получен не null')

        #изменить у actor параметр visitStatus
        actor_id = info_cell.json()['result']['actors'][0]['id']

        setvisitstatus = MyRequests.get(f'/tm-schedule/api/schedules/actors/{actor_id}/setVisitStatus?visitStatus=true', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(setvisitstatus, True, setvisitstatus.json()['result']['visitStatus'], 'Изменение статуса прошло неуспешно')

        #отменить запись
        cancel_cell = MyRequests.get(f'/tm-schedule/api/schedules/cell/{bookedcell_id}/cancel', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(cancel_cell, False, cancel_cell.json()['result']['active'], 'Полученный статус активен')

        #проверяем что запись неактивна
        info_cell_after_delete = MyRequests.get(f'/tm-schedule/api/schedules/cell/{bookedcell_id}/info',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(info_cell_after_delete, False, info_cell_after_delete.json()['result']['active'],'Полученный статус активен')
        Assertions.assert_expectedvalue_equal_receivedvalue(info_cell_after_delete, True,info_cell_after_delete.json()['result']['actors'][0]['visitStatus'],
                                                            'visitStatus получен не True')

        #удалить расписание
        delete = MyRequests.delete(f'/tm-schedule/api/schedules/{schedule_id}', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление прошло неуспешно')

        #проверяем что расписание больше неактивно
        get_schedule_after_delete = MyRequests.get(f'/tm-schedule/api/schedules/{schedule_id}',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(get_schedule_after_delete, False,get_schedule_after_delete.json()['result']['active'],'Статус расписания активен')

    @allure.feature("Проверка singleEvent")
    def test_singleevent(self):

        replace_values_schedule = {'date_from': str(date.today() + datetime.timedelta(days=1)),'date_to': str(date.today() + datetime.timedelta(days=20))}
        self.singleevent = self.multiple_replace(self.singleevent, replace_values_schedule)

        #создание singleevent
        create = MyRequests.post('/tm-schedule/api/schedules/singleEvent', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                 data=self.singleevent)
        Assertions.assert_expectedvalue_equal_receivedvalue(create, True, create.json()['result']['active'], 'singleEvent имеет неактивный статус')

        event_id = create.json()['result']['id']
        cell_id = create.json()['result']['cells'][0]['id']

        #занять ячейку полученную
        take = MyRequests.post(f'/tm-schedule/api/schedules/cell/{cell_id}/take', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                               data=self.take_cell)
        Assertions.assert_expectedvalue_equal_receivedvalue(take, True, take.json()['result']['active'], 'Занятие ячейки прошло неуспешно')

        bookedcell_id = take.json()['result']['id']

        #отменить запись
        cancel_cell = MyRequests.get(f'/tm-schedule/api/schedules/cell/{bookedcell_id}/cancel',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_expectedvalue_equal_receivedvalue(cancel_cell, False, cancel_cell.json()['result']['active'],'Полученный статус активен')

        #удалить расписание
        delete = MyRequests.delete(f'/tm-schedule/api/schedules/{event_id}',headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(delete, 'success', True, 'Удаление прошло неуспешно')

    @allure.feature("Проверка что методы поиска рабочие")
    def test_search_schedule(self):

        #получение отчета по доступным местам
        search = MyRequests.post('/tm-schedule/api/schedules/search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                 data=self.search_schedule)
        Assertions.assert_expectedvalue_equal_receivedvalue(search, '4a02a1c9-0318-4ba4-8a04-a219ec9703cd', search.json()['result']['items'][0]['id'], 'Полученный в ответе id не равен ожидаемому')

        #получение админского отчета по доступным местам
        search_admin = MyRequests.post('/tm-schedule/api/schedules/admin/search', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                       data=self.search_admin_schedule)
        Assertions.assert_expectedvalue_equal_receivedvalue(search_admin, '962f645b-589d-4657-b2bb-acbbe1c8ff62', search_admin.json()['result']['items'][0]['id'],
                                                            'Полученный в ответе id не равен ожидаемому')

        #получение спика используемых в описании расписания справочников НСИ
        nsi = MyRequests.get('/tm-schedule/api/schedules/nsi', headers={'Authorization': f'{config.token_test_practitioner}'})
        Assertions.assert_json_value_by_name(nsi, 'success', True, 'Получение списка справочников завершилось неуспешно')

        #админский поиск ячеек
        admin_cells = MyRequests.post('/tm-schedule/api/schedules/admin/cells', headers={'Content-Type': 'application/json-patch+json', 'Authorization': f'{config.token_test_practitioner}'},
                                      data=self.search_admin_cells)
        Assertions.assert_expectedvalue_equal_receivedvalue(admin_cells, 'c968e8fb-f2fc-4d7c-96df-f38830f2eb28', admin_cells.json()['result']['items'][0]['id'], 'Полученный id не равен ожидаемому')
