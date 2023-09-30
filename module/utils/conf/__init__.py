from module import home_path


def get_conf_file_path() -> str:
    return home_path() + "/config.json"
