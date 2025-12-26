FROM python:3.12.12-alpine

ENV WORK_DIR="/app/src"
ENV PYTHONPATH=${WORK_DIR}
ENV PYTHONDONTWRITEBYTECODE=1
ENV USER=keeper
ENV GROUP=keeper

WORKDIR ${WORK_DIR}

# Create user
RUN addgroup --system ${GROUP} &&\
    adduser --system --home ${WORK_DIR}/../user --ingroup ${GROUP} ${USER} --shell /bin/sh

# Install requirements
RUN pip install --no-cache-dir poetry &&\
    poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml .
RUN poetry install --only main --no-interaction --no-ansi

# Copy the sorurce
COPY docker-entrypoint.sh .
COPY telegram_session_keeper/ telegram_session_keeper/

# Apply user
RUN chown -R ${USER}:${GROUP} ${WORK_DIR}
USER ${USER}

ENTRYPOINT ["/app/src/docker-entrypoint.sh"]
