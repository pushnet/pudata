import json

from module import PUDATA_HOME


class LocalConfigLoader:
    def __init__(self):
        self.config_path = PUDATA_HOME + "/config.json"
    def get_secret_config(self, key_name: str) -> dict:
        """

        :return: {'a_api_key': '***', 'b_api_key': '***'}
        """
        with open(self.config_path) as f:
            secrets = json.load(f).get("secrets")

        return secrets.get(key_name)
