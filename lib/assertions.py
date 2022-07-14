from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'
        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_body_has_keys(data, names:list):
        try:
            for name in names:
                assert name in data, f"Response JSON doesn't have key {name}"
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {data.text}'
        for name in names:
            assert name in data, f"Response JSON doesn't have key {name}"

    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'
        assert name not in response_as_dict, f"Response JSON shouldn't have key {name}. But it's present"

    @staticmethod
    def assert_value_equeals_expected(value, expected_value):
        assert value == expected_value, f'Received value is not equals expected value'

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f'Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}'

    @staticmethod
    def assert_body(response: Response, expected_body):
        assert response.text == expected_body, \
            f'Unexpected body! Expected: {expected_body}. Actual: {response.text}'

    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_expectedvalue_equal_receivedvalue(response: Response, expected_value, received_value, error_message):
        assert expected_value == received_value, error_message
