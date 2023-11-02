from orm import SqlModuler
import logging
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
import pytz
from constants import TIMEZONE
from handler_slack import airflow_task_failure_callbacks
import requests
from models import RawApiData
import json
import pandas as pd



logger = logging.getLogger('airflow.task')

def localize_utc_tz(d):
	return pytz.timezone(TIMEZONE).fromutc(d)

default_args = {
	'email': '',
	'email_on_failure': True,
	'email_on_retry': False,
	'retries':3,
	'retry_delay':timedelta(seconds=30),
	'trigger_rule':'none_failed',
	'depends_on_past':True,
	'wait_for_downstream':False,
	"on_failure_callback": airflow_task_failure_callbacks,
	'execution_timeout':timedelta(minutes=10)
	}

user_defined_filters={
	'localtz': localize_utc_tz,
	}

@dag(dag_id='ingest_api', start_date=days_ago(1), schedule='00 12 * * *', catchup=True, max_active_tasks=6, max_active_runs=1, default_args=default_args,user_defined_filters=user_defined_filters)		
def ingest_api():

	SQLM = SqlModuler()
	  
	API_TEMPLATE = {
		'Sponsor': 'https://health-products.canada.ca/api/clinical-trial/sponsor/?lang=en&type=json',
		'Medical Condition':'https://health-products.canada.ca/api/clinical-trial/medicalcondition/?lang=en&type=json',
		'Drug Product':'https://health-products.canada.ca/api/clinical-trial/drugproduct/?lang=en&type=json',
		'Protocol':'https://health-products.canada.ca/api/clinical-trial/protocol/?lang=en&type=json',
		'Trial Status':'https://health-products.canada.ca/api/clinical-trial/status/?lang=en&type=json',
		'Study Population':'https://health-products.canada.ca/api/clinical-trial/studypopulation/?lang=en&type=json'
	}
	
	def get_api_ingestion_task(api_name, api_url):
		@task(task_id=f"api_ingestion_task__{api_name.replace(' ','_')}")
		def api_ingestion_task(**kwargs):
			resp = requests.get(api_url)
			resp_json_str = resp.content.decode("utf-8")
			logger.info(f'Response: {resp_json_str}')
			rad = RawApiData(api_name=api_name, api_url=api_url, api_data=json.loads(resp_json_str))
			rad = SQLM.insert_model_obj(rad)
			logger.info(f'API data from {api_name} is inserted')
			return True
		return api_ingestion_task
	
	@task
	def show_today_all_data(**kwargs):
		logger.info(f"Data as of {kwargs['logical_date']} is updated")
		sql = "SELECT id, ingest_timestamp, api_name, api_url, api_data FROM raw_api_data"
		df = pd.read_sql(sql, con=SQLM.engine.connect() )
		pd.set_option('display.max_columns', None)
		pd.set_option('display.max_rows', None)
		pd.set_option('display.width', 1000)
		print(df.head())
		return True
	
	all_done = show_today_all_data()

	for api_name, api_url in API_TEMPLATE.items():
		api_ingestion_task = get_api_ingestion_task(api_name, api_url)
		is_inserted = api_ingestion_task()
		is_inserted >> all_done

ingest_api_dag = ingest_api()
 