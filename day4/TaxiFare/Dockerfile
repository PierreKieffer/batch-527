FROM python:3.7-slim-buster

RUN mkdir /TaxiFare

COPY . /TaxiFare

RUN pip install -r /TaxiFare/requirements.txt

WORKDIR /TaxiFare

EXPOSE 8080 

CMD uvicorn api.server:app --host "0.0.0.0" --port 8080







