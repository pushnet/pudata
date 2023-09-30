import json

from module.utils.conf import get_conf_file_path


def get_config_values(section: str, key_name: str) -> dict:
    """

    :return: {'a_api_key': '***', 'b_api_key': '***'}
    """
    with open(get_conf_file_path(), encoding="utf-8") as file:
        secrets = json.load(file).get(section)

    return secrets.get(key_name)
