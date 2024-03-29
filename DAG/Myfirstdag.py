from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 11, 10),
    'email': ['gauthier.deville@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
 }

dag = DAG('Run airflow check',
          default_args=default_args,
          schedule_interval=timedelta(minutes=5))

process_status_web = BashOperator(task_id='ps.web.server',
                                  bash_command='ps -eaf | '
                                               'grep "master [airflow-webserver]"',
                                  dag=dag)

process_status_worker = BashOperator(task_id='ps.worker.server',
                                     bash_command='ps -eaf | '
                                                  'grep "worker [airflow-webserver]"',
                                     dag=dag)

process_status_scheduler = BashOperator(task_id='ps.scheduler.server',
                                        bash_command='ps -eaf | grep scheduler',
                                        dag=dag)

process_status_scheduler >> process_status_worker >> process_status_web
