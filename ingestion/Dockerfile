FROM python:3.7

ENV PYTHONUNBUFFERED 1
COPY requirements_ingestion.txt .
COPY weblogs.log .
COPY ingestion.py .
COPY utils.py .
RUN pip install -r requirements_ingestion.txt


CMD ["python", "ingestion.py"]
