FROM python:3.8

RUN mkdir /booking_engine
WORKDIR /booking_engine
COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
