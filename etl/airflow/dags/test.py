from datetime import datetime

from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from module.airflow.handler.telegram_handler import telegram_failure_callback, telegram_success_callback
from module.airflow.pattern.factory.dag_factory import PudataDagFactory

with PudataDagFactory().activate_success_callback().build_dag() as dag:
    t_o = BashOperator(
        task_id="test_o",
        bash_command="echo >> {{ logical_date2 }}",
    )

    _ = t_o
