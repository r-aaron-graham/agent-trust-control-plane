FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.lock .
RUN pip install --no-cache-dir -c requirements.lock -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
