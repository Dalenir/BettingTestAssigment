FROM python:3.11
WORKDIR /line-provider
RUN pip install --no-cache-dir --upgrade fastapi uvicorn python-multipart
COPY app.py app.py

ARG API_PORT
ENV API_PORT ${API_PORT}

CMD uvicorn app:app --host 0.0.0.0 --port $API_PORT