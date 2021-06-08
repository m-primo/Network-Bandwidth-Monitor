FROM python:latest

COPY app.py /
COPY reqs.txt /

RUN pip install -r reqs.txt
CMD ["python", "-u", "app.py"]