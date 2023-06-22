FROM python:3.9

WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD app /app

EXPOSE 5000

CMD ["python", "app.py"]