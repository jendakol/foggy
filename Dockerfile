FROM python:3.10-alpine

WORKDIR /foggy

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["./foggy.py"]