FROM python:3.12-slim

WORKDIR "/usr/src/"

ENV  PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VIRTUALENVS_CREATE=false 


COPY pyproject.toml poetry.lock ./

RUN python3.12 -m pip install --upgrade pip && \
    pip3 install poetry==1.8.5 && \
    poetry install --no-root

COPY . .

ENTRYPOINT ["gunicorn", "-b 0.0.0.0:8050", "rzd_planner.main:srv"]