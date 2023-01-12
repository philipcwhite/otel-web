FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV OTEL_RESOURCE_ATTRIBUTES="service.name=demo-flask"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-gateway.monitoring:4317"
ENV OTEL_TRACES_EXPORTER=otlp_proto_grpc
CMD [ "opentelemetry-instrument", "flask", "run", "--host=0.0.0.0" ]