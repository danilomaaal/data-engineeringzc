FROM python:latest

RUN apt-get install wget gzip
RUN pip install pandas psycopg2 sqlalchemy

WORKDIR app/

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]