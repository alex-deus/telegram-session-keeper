FROM python:3.12.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV WORK_DIR "/app"
ENV USER keeper
ENV GROUP keeper

EXPOSE 5555
EXPOSE 8000

WORKDIR ${WORK_DIR}

RUN addgroup --system ${GROUP} &&\
    adduser --system --home ${WORK_DIR}/../user --ingroup ${GROUP} ${USER} --shell /bin/bash &&\
    chown -R ${USER}:${GROUP} ${WORK_DIR}/..

RUN pip install --no-cache-dir poetry &&\
    poetry config virtualenvs.create false
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["/app/docker-entrypoint.sh"]
