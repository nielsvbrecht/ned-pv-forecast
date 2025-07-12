FROM python:3.12-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./app/

COPY pv-forecast-addon/config.json .

ENTRYPOINT ["python", "app/main.py"]
