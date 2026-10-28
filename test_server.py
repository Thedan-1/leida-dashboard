"""Regression tests for the local proxy's request boundaries."""

from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from typing import Optional

import server


class ProxySecurityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original_api_key = server.API_KEY
        server.API_KEY = ""
        cls.httpd = server.socketserver.ThreadingTCPServer(
            ("127.0.0.1", 0), server.ProxyHTTPRequestHandler
        )
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.httpd.server_address[1]}/api/chat"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()
        server.API_KEY = cls.original_api_key

    def request(self, body: bytes, content_length: Optional[str] = None) -> urllib.request.Request:
        headers = {"Content-Type": "application/json"}
        if content_length is not None:
            headers["Content-Length"] = content_length
        return urllib.request.Request(self.url, data=body, headers=headers, method="POST")

    def test_missing_api_key_is_explicit(self) -> None:
        server.API_KEY = ""
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(self.request(b"{}"), timeout=2)
        self.assertEqual(context.exception.code, 503)
        payload = json.loads(context.exception.read().decode("utf-8"))
        self.assertEqual(payload["error"], "BAIDU_API_KEY is not configured")

    def test_invalid_json_is_rejected_before_upstream_call(self) -> None:
        server.API_KEY = "unit-test-key"
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(self.request(b"not-json"), timeout=2)
        self.assertEqual(context.exception.code, 400)

    def test_oversized_request_is_rejected(self) -> None:
        server.API_KEY = "unit-test-key"
        oversized = server.MAX_BODY_BYTES + 1
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(self.request(b"{}", str(oversized)), timeout=2)
        self.assertEqual(context.exception.code, 413)


if __name__ == "__main__":
    unittest.main()
