FROM python:3.8-slim 

RUN mkdir app 

COPY . /app 

RUN pip install -r /app/requirements.txt

WORKDIR /app 

CMD streamlit run webapp.py --server.port 8080 


