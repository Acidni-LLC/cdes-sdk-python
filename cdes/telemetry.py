'''CDES Telemetry - Privacy-respecting usage analytics.'''

import os
import uuid
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
from functools import wraps

TELEMETRY_ENABLED = os.environ.get("CDES_TELEMETRY", "1").lower() not in ("0", "false", "no", "off")
TELEMETRY_ENDPOINT = os.environ.get("CDES_TELEMETRY_ENDPOINT", "https://cdes.acidni.net/api/telemetry")

_session_id: Optional[str] = None
_events: list = []

def _get_session_id() -> str:
    global _session_id
    if _session_id is None:
        _session_id = str(uuid.uuid4())
    return _session_id

def _get_install_id() -> str:
    '''Get anonymous install ID (hashed machine identifier).'''
    try:
        machine = os.environ.get("COMPUTERNAME", os.environ.get("HOSTNAME", "unknown"))
        user = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
        raw = f"{machine}:{user}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]
    except:
        return "anonymous"

def track_event(event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
    '''Track a usage event (only if telemetry enabled).'''
    if not TELEMETRY_ENABLED:
        return
    event = {
        "event": event_name,
        "timestamp": datetime.utcnow().isoformat(),
        "session_id": _get_session_id(),
        "install_id": _get_install_id(),
        "properties": properties or {},
    }
    _events.append(event)
    # Batch send in background (implement async later)

def track_import(module_name: str) -> None:
    '''Track module import.'''
    track_event("import", {"module": module_name})

def track_validation(schema_type: str, valid: bool) -> None:
    '''Track validation call.'''
    track_event("validate", {"schema": schema_type, "valid": valid})

def track_model_usage(model_name: str, method: Optional[str] = None) -> None:
    '''Track model class usage.'''
    props = {"model": model_name}
    if method:
        props["method"] = method
    track_event("model_usage", props)

def tracked(event_name: str):
    '''Decorator to track function calls.'''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            track_event(event_name, {"function": func.__name__})
            return func(*args, **kwargs)
        return wrapper
    return decorator

def get_tracked_events() -> list:
    '''Get all tracked events (for debugging).'''
    return _events.copy()

def disable_telemetry() -> None:
    '''Disable telemetry for this session.'''
    global TELEMETRY_ENABLED
    TELEMETRY_ENABLED = False

def enable_telemetry() -> None:
    '''Enable telemetry for this session.'''
    global TELEMETRY_ENABLED
    TELEMETRY_ENABLED = True
