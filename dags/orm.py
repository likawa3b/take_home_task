from sqlalchemy import create_engine
from constants import DB_CONFIGS
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class SqlModuler:

	def __init__(self, connection_name='data_lakehouse'):
		self.db_config = DB_CONFIGS.get(connection_name)
		self.engine = create_engine(f'postgresql+psycopg2://{self.db_config["USER"]}:{self.db_config["PASSWORD"]}@{self.db_config["HOST"]}:{self.db_config["PORT"]}/{self.db_config["DB"]}', pool_pre_ping=True, echo=True)

	@contextmanager
	def get_session(self, expire_on_commit=True):
		Session = sessionmaker()
		session = Session(bind=self.engine, expire_on_commit=expire_on_commit)
		try:
			yield session
		except Exception as e:
			session.rollback()
			raise e
		else:
			session.commit()
	
	def insert_model_obj(self, *objs, expire_on_commit=False):
		with self.get_session(expire_on_commit) as session:
			refreshed_objs = []
			for obj in objs:
				session.add(obj)
				session.commit()
				session.refresh(obj)
				refreshed_objs.append(obj)
			if len(refreshed_objs) ==1:
				return refreshed_objs[0]
			else:
				return refreshed_objs