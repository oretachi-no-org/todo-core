FROM python:3.8-buster
RUN mkdir -p /code
ENV TODO_CORE_OVERRIDE=development
COPY . /code/
WORKDIR /code
RUN set -ex; \
    python -m pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

