from pathlib import Path
import pandas as pd
import os

TABLE_NAMES = {
    "pai_group_tag_table",
    "pai_instance_table",
    "pai_job_table",
    "pai_machine_metric",
    "pai_machine_spec",
    "pai_sensor_table",
    "pai_task_table"
}




def check_table_name(table_name):
    assert table_name in TABLE_NAMES, f"{table_name} is not a table name"


def get_header_path(table_name):
    check_table_name(table_name)
    return os.path.join("..", "..", "cluster-trace-gpu-v2020", "data", table_name + ".header")


def get_data_path(table_name):
    check_table_name(table_name)
    return os.path.join("..", "data", table_name + ".csv")


def load_table(table_name):
    header = Path(get_header_path(table_name)).read_text().strip().split(",")
    return pd.read_csv(get_data_path(table_name), names=header)


def load_tasks():
    tasks = load_table("pai_task_table")
    tasks = tasks[tasks['status'] != 'Waiting']
    tasks = tasks[['job_name', 'start_time', 'end_time', 'plan_gpu']]
    tasks[['start_time', 'end_time']] = tasks[[
        'start_time', 'end_time']].astype("Int64")
    tasks['plan_gpu'] /= 100
    tasks = tasks.rename(columns={'plan_gpu': 'gpus'})
    tasks = tasks.dropna(subset=['gpus'])
    return tasks


