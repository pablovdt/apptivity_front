FROM python:3.11-slim

WORKDIR /apptivity_front

COPY . /apptivity_front

COPY ./images /app/images

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV BACKEND_URL=http://apptivity:8000/

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
