FROM python:3.8-buster
RUN mkdir -p /code
ENV TODO_CORE_OVERRIDE=development

# Because of this step don't use in public network.
ENV TODO_CORE_SECRET_KEY=^oe(y^!d7pz(7-34gd6za7zzw#rx0n(wfi7vj-zr4y9od@4pk7
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN set -ex; \
    python -m pip install -r requirements.txt

EXPOSE 8000
COPY . /code/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

