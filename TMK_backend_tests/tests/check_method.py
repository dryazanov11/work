import json

import config
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Базовые проверки сервисов ТМ")
class TestCheckMethod():
    def setup(self):
        self.expected_fields = ["serviceVersion", "databaseVersion", "buildDate"]
        self.expected_fields_lpu = ["resourceType", "parameter"]
        self.expected_fields_iemk = ["encounterId", "periodStart", "periodEnd", "daysCount",
                                     "serviceProvider", "doctorName", "doctorSpeciality", "documentReference"]

    @allure.feature("Проверка tm.core")
    def test_tm_core(self):
        response = MyRequests.get('/tm-core/api/_version')
        Assertions.assert_json_has_keys(response, self.expected_fields)
        Assertions.assert_code_status(response, 200)

    @allure.feature("Проверка tm.plugins")
    def test_tm_plugins(self):
        response = MyRequests.get('/tm-plugins/ping')
        Assertions.assert_code_status(response, 200)
        Assertions.assert_body(response, 'pong')

    @allure.feature("Проверка tm.schedule")
    def test_tm_schedule(self):
        response = MyRequests.get('/tm-schedule/api/_version')
        Assertions.assert_json_has_keys(response, self.expected_fields)
        Assertions.assert_code_status(response, 200)

    @allure.feature("Проверка tm.widgets")
    @allure.story("Проверка версии tm.widgets")
    def test_tm_widgets_version(self):
        response = MyRequests.get('/tm-schedule/api/_version')
        Assertions.assert_json_has_key(response, self.expected_fields[0])
        Assertions.assert_json_has_key(response, self.expected_fields[2])
        Assertions.assert_code_status(response, 200)

    #@allure.description("Проверка tm.widgets")
    #@allure.story("Проверка связи с НСИ")
    #def test_tm_widgets_nsi(self):
        #Выполнить запрос на прямую в НСИ для получения списка справочников используя конфигурации tm.widgets

    @allure.feature("Проверка tm.widgets")
    @allure.story("Проверка связи со справочниками НСИ")
    def test_tm_widgets_nsi_dictionaries(self):
        response = MyRequests.get('/tm-widgets/api/nsi/Dictionaries', headers={'accept': 'application/fhir+json'})
        Assertions.assert_json_value_by_name(response, 'resourceType', 'Parameters', 'Справочники не найдены')
        Assertions.assert_code_status(response, 200)

    #@allure.description("Проверка tm.widgets")
    #@allure.story("Проверка связи с MPI")
    #def test_tm_widgets_mpi(self):
        #Выполнить запрос на прямую в MPI для получения карточки пациента используя конфигурации tm.widgets

        #Выполнить запрос  <base_url>/tm-widgets/api/Mpi/GetPatientCardById/<patientId>, пока приводит к ошибке 404
        #response = MyRequests.get(f'/tm-widgets/api/Mpi/GetPatientCardById/{config.patientId}')
        #Assertions.assert_code_status(response, 200)

    @allure.feature("Проверка tm.widgets")
    @allure.story("Проверка поиска организации в НСИ")
    def test_tm_widgets_search_mo_nsi(self):
        #Выполнить запрос на прямую в НСИ для получения данных об организации используя конфигурации tm.widgets

        response = MyRequests.get(f'/tm-widgets/api/nsi/SearchOrganization?code={config.idLpu}')
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, self.expected_fields_lpu)

    @allure.description("Проверка tm.widgets")
    @allure.story("Проверка связи с ИЭМК")
    def test_tm_widgets_connect_iemk(self):
        #Выполнить запрос на прямую в ИЭМК для получения результатов поиска СМО используя конфигурации tm.widgets

        response = MyRequests.get(f'/tm-widgets/api/MedicalCareCases/Encounters?patientId={config.patientId}')
        Assertions.assert_code_status(response, 200)
        Assertions.assert_body_has_keys(response.json()['result'][0], self.expected_fields_iemk)

    @allure.description("Проверка tm.widgets")
    @allure.story("Проверка связи с ОДЛИ")
    def test_tm_widgets_connect_odli(self):
        #Выполнить запрос на прямую в ОДЛИ для получения результатов исследования пациента используя конфигурации tm.widgets

        response = MyRequests.get(f'/tm-widgets/api/LaboratoryResearches/List?mpiPatientId={config.patientId}')
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, response.json()[0])

    #@allure.description("Проверка tm.widgets")
    #@allure.story("Проверка связи с ОДИИ")
    #def test_tm_widgets_connect_odii(self):
    #Выполнить запрос на прямую в ОДИИ для получения результатов исследования пациента используя конфигурации tm.widgets

    #Выполнить запрос  <base_url>/tm-widgets /api/InstrumentalResearches/List?mpiPatientId=<patientId>, пока отвечает 500 c текстом о 403

    @allure.description("Проверка tm.widgets")
    @allure.story("Проверка связи с УО")
    def test_tm_widgets_connect_mq(self):
    #Выполнить запрос на прямую в УО для получения направления пациента используя конфигурации tm.widgets

        response = MyRequests.get(f'/tm-widgets/api/Uo/List?mpiPatientId={config.patientId}')
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, response.json()[0])

    @allure.feature("Проверка tm.settings")
    def test_tm_schedule(self):
        response = MyRequests.get('/tm-settings/api/_version')
        Assertions.assert_json_has_keys(response, self.expected_fields)
        Assertions.assert_code_status(response, 200)

