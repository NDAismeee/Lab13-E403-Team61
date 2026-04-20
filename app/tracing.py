from __future__ import annotations

import os
import sys
from typing import Any

LANGFUSE_IMPORT_ERROR: str | None = None
LANGFUSE_VERSION: str | None = None
LANGFUSE_FILE: str | None = None

try:
    import langfuse as _langfuse_mod
    from langfuse import get_client, observe
    try:
        LANGFUSE_VERSION = getattr(_langfuse_mod, "__version__", None)
        LANGFUSE_FILE = getattr(_langfuse_mod, "__file__", None)
    except Exception:
        LANGFUSE_VERSION = None
        LANGFUSE_FILE = None
except Exception as e:  # fail loudly in health/startup
    _langfuse_mod = None  # type: ignore
    get_client = None  # type: ignore

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    LANGFUSE_IMPORT_ERROR = repr(e)


def tracing_configured() -> bool:
    return bool(
        os.getenv("LANGFUSE_PUBLIC_KEY")
        and os.getenv("LANGFUSE_SECRET_KEY")
        and os.getenv("LANGFUSE_BASE_URL")
    )


_CLIENT: Any | None = None


def get_langfuse_client() -> Any | None:
    global _CLIENT
    if get_client is None:
        return None
    if _CLIENT is not None:
        return _CLIENT
    try:
        _CLIENT = get_client()
        return _CLIENT
    except Exception:
        return None


def tracing_ready() -> bool:
    if not tracing_configured():
        return False
    client = get_langfuse_client()
    if client is None:
        return False
    try:
        return bool(client.auth_check())
    except Exception:
        return False


def get_tracing_status() -> dict[str, Any]:
    return {
        "configured": tracing_configured(),
        "ready": tracing_ready(),
        "import_error": LANGFUSE_IMPORT_ERROR,
        "python_executable": sys.executable,
        "langfuse_version": LANGFUSE_VERSION,
        "langfuse_file": LANGFUSE_FILE,
    }


def safe_update_current_observation(**kwargs: Any) -> None:
    try:
        client = get_langfuse_client()
        if client is None:
            return

        if "usage_details" in kwargs:
            try:
                client.update_current_generation(**kwargs)
                return
            except Exception:
                pass

        try:
            client.update_current_span(**kwargs)
            return
        except Exception:
            pass

        try:
            client.update_current_trace(**kwargs)
        except Exception:
            return
    except Exception:
        return


def safe_score_current_observation(name: str, value: float, **kwargs: Any) -> None:
    try:
        client = get_langfuse_client()
        if client is None:
            return

        try:
            client.score_current_span(name=name, value=value, **kwargs)
            return
        except Exception:
            pass

        try:
            client.score_current_trace(name=name, value=value, **kwargs)
        except Exception:
            return
    except Exception:
        return


def safe_flush() -> None:
    client = get_langfuse_client()
    if client is None:
        return
    try:
        client.flush()
    except Exception:
        return