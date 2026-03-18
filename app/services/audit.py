from __future__ import annotations

from datetime import datetime
from threading import Lock

from app.models.domain import AuditEvent


class AuditService:
    """
    In-memory audit store.

    Replace with persistent storage for production use.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._events: dict[str, AuditEvent] = {}

    def record(self, event: AuditEvent) -> None:
        with self._lock:
            self._events[event.trace_id] = event

    def get(self, trace_id: str) -> AuditEvent | None:
        return self._events.get(trace_id)

    def list(self) -> list[AuditEvent]:
        return sorted(
            self._events.values(),
            key=lambda event: event.timestamp,
            reverse=True,
        )
