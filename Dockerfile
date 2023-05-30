FROM python:3.9

RUN apt update -y
RUN apt install python3 pip -y
RUN pip install boto3 wheel
WORKDIR /app
COPY app.py .
COPY menu.py .
COPY functions.py .
ENTRYPOINT ["python", "app.py"]