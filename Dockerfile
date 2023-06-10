FROM python:3.11

COPY /app /app
COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]