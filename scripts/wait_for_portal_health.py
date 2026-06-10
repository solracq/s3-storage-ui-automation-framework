"""
Wait for the Secure S3 File Portal health endpoint to become ready.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the health wait helper.
    """
    parser = argparse.ArgumentParser(
        description="Wait for the portal /health endpoint to become available.",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:8000",
        help="Portal base URL to probe. Defaults to http://localhost:8000.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=90,
        help="Maximum number of seconds to wait before failing.",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=float,
        default=2.0,
        help="Delay between health checks while waiting.",
    )
    parser.add_argument(
        "--require-storage-ready",
        action="store_true",
        help="Require /health to report storage_ready=true before succeeding.",
    )
    return parser.parse_args()


def read_health_payload(base_url: str) -> dict[str, object]:
    """
    Read the JSON payload from the portal health endpoint.
    """
    normalized_base_url = base_url.rstrip("/")
    with urlopen(f"{normalized_base_url}/health", timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_health(
    *,
    base_url: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
    require_storage_ready: bool,
) -> dict[str, object]:
    """
    Poll the health endpoint until the portal reaches the expected readiness state.
    """
    deadline = time.monotonic() + timeout_seconds
    last_payload: dict[str, object] | None = None
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        try:
            payload = read_health_payload(base_url)
            last_payload = payload

            if require_storage_ready:
                if payload.get("storage_ready") is True:
                    return payload
            elif payload.get("status") in {"ok", "degraded"}:
                return payload
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc

        time.sleep(poll_interval_seconds)

    expected_state = (
        "storage_ready=true"
        if require_storage_ready
        else "an available /health response"
    )
    if last_payload is not None:
        raise TimeoutError(
            f"Timed out waiting for {expected_state}. Last health payload: {last_payload!r}."
        )

    raise TimeoutError(
        f"Timed out waiting for {expected_state}. Last error: {last_error!r}."
    )


def main() -> None:
    """
    Wait for the configured portal health state and print the final payload.
    """
    args = parse_args()
    payload = wait_for_health(
        base_url=args.base_url,
        timeout_seconds=args.timeout_seconds,
        poll_interval_seconds=args.poll_interval_seconds,
        require_storage_ready=args.require_storage_ready,
    )

    print("Portal health check succeeded.")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
