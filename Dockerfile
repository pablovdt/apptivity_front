FROM python:3.9-slim

RUN apt-get update && apt-get install -y locales

RUN locale-gen es_ES.UTF-8
RUN update-locale LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8

ENV LANG es_ES.UTF-8
ENV LC_ALL es_ES.UTF-8

WORKDIR /apptivity_front

COPY . /apptivity_front

COPY ./images /app/images

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV BACKEND_URL=http://apptivity:8000/

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
