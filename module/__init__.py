import os

PUDATA_HOME_ENV = "PUDATA_HOME"


def home_path() -> str:
    if PUDATA_HOME_ENV not in os.environ:
        raise ValueError("Please register 'PUDATA_HOME' environment variable.")

    return os.environ[PUDATA_HOME_ENV]
