FROM python:3

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app" , "--reload", "--host", "0.0.0.0"]
