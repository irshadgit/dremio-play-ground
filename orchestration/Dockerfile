FROM apache/airflow:2.0.2

ARG AIRFLOW_HOME="/opt/airflow"

USER root
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev python3-dev python3-pip wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ${AIRFLOW_HOME}
WORKDIR ${AIRFLOW_HOME}
RUN pip install -r requirements.txt
USER airflow