FROM python:3.8-buster
RUN mkdir -p /code
ENV TODO_CORE_OVERRIDE=development
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN set -ex; \
    python -m pip install -r requirements.txt

EXPOSE 8000
COPY . /code/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

