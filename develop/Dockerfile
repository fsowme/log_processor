FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHON_VERSION=3.12

ADD ../requirements/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /project
ADD ../src .

ENTRYPOINT ["gunicorn", "log_processor.wsgi", "--bind", "0.0.0.0:8000", "--reload"]
EXPOSE 8000
