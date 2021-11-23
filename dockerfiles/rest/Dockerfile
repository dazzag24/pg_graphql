FROM python:3.8

RUN apt-get update -y

RUN pip install -U pip wheel setuptools toml

COPY setup.py .
COPY graphql_server.py .

RUN pip install -e .

EXPOSE 8000

CMD ["uvicorn", "graphql_server:app", "--host=0.0.0.0"]
