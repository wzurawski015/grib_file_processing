# Ścieżka: grib_processing/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "process_grib.py"]
