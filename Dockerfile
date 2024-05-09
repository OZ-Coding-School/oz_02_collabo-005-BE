FROM python:3.12

ENV PYTHONUNBUFFERED 1

LABEL maintainer="newbission"

COPY ./poetry.lock /okivery/
COPY ./pyproject.toml /okivery/
WORKDIR /okivery

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app /okivery/app
WORKDIR /okivery/app

COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh
CMD ["/scripts/run.sh"]