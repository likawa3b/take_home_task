TIMEZONE = "America/Toronto"

DB_CONFIGS = {
	'data_lakehouse':{
		"HOST":'host.docker.internal',
		"PORT":5432,
		"USER":'airflow',
		"PASSWORD":'airflow',
		"DB":'data_lakehouse',
	},
}

SLACK_BOT_TOKEN = '' 
SLACK_CHANNEL_ID = ''