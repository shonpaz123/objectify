FROM python:3.6.9-slim-buster
WORKDIR /usr/src/app
COPY ./ .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "./app.py"]
