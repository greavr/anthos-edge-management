FROM python:3-slim

LABEL maintainer="rgreaves@google.com"

COPY /src /app

WORKDIR /app
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]