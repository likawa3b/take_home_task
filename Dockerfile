FROM apache/airflow:2.7.2-python3.10

ENV TZ="America/Toronto"

COPY requirements.txt ./requirements.txt
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY dags ./dags

RUN pip install -r requirements.txt

RUN alembic upgrade head