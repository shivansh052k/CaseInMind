"""OpenTelemetry instrumentation setup.

Every agent step, LLM call, tool call, and ranking score gets traced as
a span through get_tracer(). Metrics (request counts, latency, token
usage, guardrail triggers) go through `meter`. Both export to the OTel
Collector, which routes traces to Arize Phoenix and metrics to
Prometheus (see docker/docker-compose.yml).
"""

from __future__ import annotations

import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_initialized = False


def _init() -> None:
    global _initialized
    if _initialized:
        return

    service_name = os.environ.get("OTEL_SERVICE_NAME", "caseinmind")
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    resource = Resource.create({SERVICE_NAME: service_name})

    # Traces
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(tracer_provider)

    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=endpoint, insecure=True)
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    _initialized = True


def get_tracer(name: str):
    """Get a tracer for the given module/component name."""
    _init()
    return trace.get_tracer(name)


def get_meter(name: str):
    """Get a meter for the given module/component name, for custom metrics."""
    _init()
    return metrics.get_meter(name)


# Module-level default meter for convenience, per the spec's `meter` export.
_init()
meter = metrics.get_meter(os.environ.get("OTEL_SERVICE_NAME", "caseinmind"))
