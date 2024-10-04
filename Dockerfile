FROM python:3.12.3-alpine3.20

WORKDIR /app

copy requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /src /app

CMD ["fastapi", "run","--host", "0.0.0.0","--port", "8000"]

