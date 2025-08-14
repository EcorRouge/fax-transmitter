FROM ecorrouge/rococo-service-host:python-3.11

WORKDIR /app/src/services/fax_transmitter

COPY pyproject.toml poetry.lock* README.md ./

COPY ./pyproject.toml /app/pyproject.toml

RUN poetry lock && poetry install --no-root

COPY ./src ./src
COPY ./tests ./tests

WORKDIR /app

ENV PYTHONPATH /app

ENV MESSAGING_TYPE=RabbitMqConnection
ENV PROCESSOR_TYPE=FaxServiceProcessor
ENV PROCESSOR_MODULE=services.fax_transmitter.src.fax_processor

COPY ./docker-entrypoint.sh ./
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh", "-l", "-c"]
