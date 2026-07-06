"""Send one test span to verify the observability stack is wired correctly.

Run after `docker compose -f docker/docker-compose.yml up -d`:

    uv run python scripts/send_test_span.py

Then check http://localhost:6006 in Arize Phoenix — you should see a
span named "phase0.smoke_test" under the "caseinmind" service.
"""

import time

from backend.observability.tracer import get_tracer

tracer = get_tracer(__name__)

with tracer.start_as_current_span("phase0.smoke_test") as span:
    span.set_attribute("phase", "0")
    span.set_attribute("purpose", "verify otel -> collector -> phoenix pipeline")
    time.sleep(0.1)

print("Test span sent. Check http://localhost:6006 in a few seconds.")
