import logging
import traceback
from constants import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID
from logging import FATAL, ERROR, WARN, INFO, DEBUG, NOTSET
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def airflow_task_failure_callbacks(context):
	if not SLACK_BOT_TOKEN:
		return
	dag_run = context.get("dag_run")
	task_id = context['task'].task_id
	log_url = dag_run.get_task_instance({task_id}).log_url

	exception = context.get('exception')
	formatted_exception = ''.join(
	traceback.format_exception(exception, 
		value=exception, tb=exception.__traceback__
	)
	).strip()

	telegram_msg = f"""
	Exception Catched in Task!
	Dag ID: {dag_run.dag_id}
	Run ID: {dag_run.run_id}
	Task ID: {task_id}
	Loggings: {log_url}

	Exception Detail: 
	{formatted_exception}
	"""

	client = WebClient(SLACK_BOT_TOKEN)

	try:
		# Call the conversations.list method using the WebClient
		result = client.chat_postMessage(
			channel=SLACK_CHANNEL_ID,
			text=telegram_msg
			# You could also use a blocks[] array to send richer content
		)
		# Print result, which includes information about the message (like TS)
		print(result)

	except SlackApiError as e:
		print(f"Error: {e}")

# class TelegramLogHandler(logging.Handler):
# 	def __init__(self, level = logging.DEBUG):
# 		super().__init__(level)
# 		formatter = logging.Formatter("%(asctime)s")
# 		self.setFormatter(formatter)
# 		self.bot = Bot(token=TELEGRAM_BOT_TOKEN) 
	
# 	def airflow_task_failure_callback(self, context):
# 		dag_run = context.get("dag_run")
# 		task_id = context['task'].task_id
# 		log_url = dag_run.get_task_instance({task_id}).log_url

# 		exception = context.get('exception')
# 		formatted_exception = ''.join(
# 		traceback.format_exception(etype=type(exception), 
# 			value=exception, tb=exception.__traceback__
# 		)
# 		).strip()

# 		telegram_msg = f"""
# 		Exception Catched in Task!
# 		Exception Detail: {formatted_exception}
# 		Dag ID: {dag_run.dag_id}
# 		Run ID: {dag_run.run_id}
# 		Task ID: {task_id}
# 		Log: {log_url}
# 		"""
# 		self.bot(token=TELEGRAM_BOT_TOKEN).send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=telegram_msg)

# 	def emit(self, record):
# 		if record.levelno>=ERROR:
# 			self.format(record)
# 			if record.levelno>=30 and (record.exc_info and record.exc_info[0] != AssertionError or not record.exc_info):
# 				path_info = "\n" + f'File "{record.pathname}", line {record.lineno}'
# 			else:
# 				path_info = ""
# 			msg = f'[{record.asctime}]  [{record.levelname}]	{record.getMessage()}{path_info}'
# 			# print(msg)

# 			# traceback_info = ''
# 			# traceback_obj = None
# 			# # f_locals = ''

# 			# if record.exc_info and record.exc_info[0] != AssertionError:
# 			# 	traceback_obj = record.exc_info[2]
# 			# 	traceback_list = traceback.format_list(traceback.extract_tb(traceback_obj))
# 			# 	traceback_info = "".join(traceback_list)
# 			# 	# print(traceback_info)

# 			telegram_msg = msg
# 			# if traceback_info:
# 			# 	telegram_msg += '\n' + traceback_info
# 			if len(telegram_msg)>4096: # Telegram message size limit
# 				telegram_msg = telegram_msg[:4096]
# 			self.bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=telegram_msg)



