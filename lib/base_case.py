import json.decoder
from requests import Response

class BaseCase:
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        return response_as_dict[name]

    def multiple_replace(self, target_str, replace_values):
        for i, j in replace_values.items():
            target_str = target_str.replace(i, j)
        return target_str