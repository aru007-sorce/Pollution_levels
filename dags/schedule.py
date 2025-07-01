from datetime import timedelta
from datetime import datetime as dtime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
from services.Final_def import run_etl  

def_args = {
    "owner": "airflow",
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "start_date": dtime(2025, 6, 25)
}

with DAG("ex_etl_dag", 
         default_args=def_args,
         catchup=False,
         schedule_interval="@daily") as dag:
    
    start = EmptyOperator(task_id="Start")
    
    e_t_l = PythonOperator(
        task_id="EXTRACT_TRANSFORM_LOAD",
        python_callable=run_etl
    )
    
    end = EmptyOperator(task_id="End")
    
    start >> e_t_l >> end
