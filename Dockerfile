FROM python:3.9.18

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

CMD ["python3"]
