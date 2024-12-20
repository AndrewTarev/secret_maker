FROM python:3.7

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["gunicorn", "main:app", "--workers 4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]