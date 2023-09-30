import logging

from airflow import DAG
from airflow.models import DagRun, TaskInstance
from airflow.utils.state import TaskInstanceState

from module.airflow.conf import AirflowConf
from module.utils.connector.telegram_connector import TelegramConnector, TELEGRAM_PUSHNET_GROUP_TOPIC_NAME_TO_THREAD_ID

logger = logging.getLogger()


def telegram_success_callback(content):
    token = AirflowConf.get_variable("telegram_pushnet_airflow_bot_token")
    chat_id = AirflowConf.get_variable("telegram_pushnet_chat_id")

    telegram_connector = TelegramConnector(token, chat_id)
    telegram_connector.send_message(
        text="success", message_thread_id=TELEGRAM_PUSHNET_GROUP_TOPIC_NAME_TO_THREAD_ID.get("success_callback")
    )


def telegram_failure_callback(content):
    token = AirflowConf.get_variable("telegram_pushnet_airflow_bot_token")
    chat_id = AirflowConf.get_variable("telegram_pushnet_chat_id")

    dag: DAG = content.get("dag")
    dag_run: DagRun = content.get("dag_run")
    logical_date = dag.timezone.convert(dag_run.logical_date)
    msg = f"{dag.dag_id} | {logical_date}\n\n"

    task_instances: list[TaskInstance] = dag_run.get_task_instances()
    fail_task_instances = [ti for ti in task_instances if ti.current_state() == TaskInstanceState.FAILED]

    for fail_task_instance in fail_task_instances:
        task_id = fail_task_instance.task_id
        log_url = fail_task_instance.log_url

        if log_url.find("localhost") != -1:
            log_url = log_url.replace("localhost", "127.0.0.1")
        msg += f"- {task_id} | <a href='{log_url}'>Log_URL</a>\n"

    logger.info(msg)
    telegram_connector = TelegramConnector(token, chat_id)
    telegram_connector.send_message(
        text=msg,
        message_thread_id=TELEGRAM_PUSHNET_GROUP_TOPIC_NAME_TO_THREAD_ID.get("failure_callback"),
    )
