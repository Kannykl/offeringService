FROM python:3.10-slim

ARG DEV=false
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN if ["$DEV" == "true"]; then poetry install --with dev; else poetry install --only main ; fi

COPY . .

CMD python -m offer