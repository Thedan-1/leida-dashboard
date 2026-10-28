"""Local proxy for the Leida Dashboard AI assistant.

The proxy keeps the Baidu credential on the local server and deliberately
accepts only bounded JSON requests. It is intended for local development, not
for exposing directly to the public internet.
"""

from __future__ import annotations

import http.server
import json
import os
import socketserver
import urllib.error
import urllib.request
from typing import Any, Optional

PORT = int(os.environ.get("LEIDA_PORT", "8000"))
API_URL = "https://aistudio.baidu.com/llm/lmapi/v3/chat/completions"
API_KEY = os.environ.get("BAIDU_API_KEY", "")
ALLOWED_ORIGIN = os.environ.get("LEIDA_ALLOWED_ORIGIN", f"http://localhost:{PORT}")
MAX_BODY_BYTES = 1 * 1024 * 1024
UPSTREAM_TIMEOUT_SECONDS = 30


def json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def write_json(handler: http.server.BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    body = json_bytes(payload)
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
    handler.send_header("Vary", "Origin")
    handler.end_headers()
    handler.wfile.write(body)


class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve the dashboard and proxy only the AI endpoint."""

    def _read_body(self) -> Optional[bytes]:
        raw_length = self.headers.get("Content-Length")
        try:
            content_length = int(raw_length or "0")
        except ValueError:
            write_json(self, 400, {"error": "Content-Length must be an integer"})
            return None

        if content_length < 0 or content_length > MAX_BODY_BYTES:
            write_json(self, 413, {"error": f"Request body exceeds {MAX_BODY_BYTES} bytes"})
            return None
        return self.rfile.read(content_length)

    def do_POST(self) -> None:  # noqa: N802 (http.server API)
        if self.path != "/api/chat":
            self.send_error(404)
            return
        if not API_KEY:
            write_json(self, 503, {"error": "BAIDU_API_KEY is not configured"})
            return

        post_data = self._read_body()
        if post_data is None:
            return
        try:
            json.loads(post_data)
        except json.JSONDecodeError:
            write_json(self, 400, {"error": "Request body must be valid JSON"})
            return

        request = urllib.request.Request(
            API_URL,
            data=post_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=UPSTREAM_TIMEOUT_SECONDS) as response:
                response_data = response.read(MAX_BODY_BYTES + 1)
                if len(response_data) > MAX_BODY_BYTES:
                    write_json(self, 502, {"error": "Upstream response is too large"})
                    return
                self.send_response(response.status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(response_data)))
                self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
                self.send_header("Vary", "Origin")
                self.end_headers()
                self.wfile.write(response_data)
        except urllib.error.HTTPError as error:
            # Preserve the upstream status but avoid leaking a traceback.
            detail = error.read(MAX_BODY_BYTES).decode("utf-8", errors="replace")
            write_json(self, error.code, {"error": "Upstream API request failed", "detail": detail})
        except (urllib.error.URLError, TimeoutError) as error:
            write_json(self, 502, {"error": "Unable to reach upstream API", "detail": str(error)})

    def do_OPTIONS(self) -> None:  # noqa: N802 (http.server API)
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Vary", "Origin")
        self.end_headers()


def run_server() -> None:
    if not API_KEY:
        print("WARNING: BAIDU_API_KEY is not set. /api/chat will return 503 until it is configured.")
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Open http://localhost:{PORT}/dashboard_system.html to view dashboard")
    server = socketserver.ThreadingTCPServer(("", PORT), ProxyHTTPRequestHandler)
    server.daemon_threads = True
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
