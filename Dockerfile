FROM python:3.10-alpine

WORKDIR /app
COPY requirements.stage.txt .
RUN python3 -m pip install pip --upgrade 
RUN python3 -m pip install -r requirements.stage.txt 

USER 1000

COPY ./src ./src

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "src.main:app", "--host", "0.0.0.0"]

