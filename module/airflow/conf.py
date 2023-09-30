from airflow import AirflowException
from airflow.models import variable


class AirflowConf:
    @staticmethod
    def get_variable(key: str) -> str:
        value = variable.Variable.get(key)

        if value is None:
            raise AirflowException("key name is not registry.")
        return value
