FROM python:latest

RUN pip install pandas psycopg2 sqlalchemy

WORKDIR app/

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]