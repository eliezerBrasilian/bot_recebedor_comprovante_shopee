FROM python:3.11-slim
WORKDIR /app

COPY api ./api
COPY classes ./classes
COPY utils ./utils
COPY main.py .

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python","main.py"]