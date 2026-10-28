"""Optional connectivity check for the Baidu ERNIE endpoint.

The test is skipped when no credential is configured. It never contains a
real token, so running the repository test suite cannot leak or revoke a
developer's key.
"""

from __future__ import annotations

import json
import os
import unittest
import urllib.error
import urllib.request

API_URL = "https://aistudio.baidu.com/llm/lmapi/v3/chat/completions"


def request_ernie(api_key: str, timeout: float = 10.0) -> dict:
    payload = {
        "model": "ernie-x1.1-preview",
        "messages": [{"role": "user", "content": "你好，请回复‘API连接成功’"}],
        "stream": False,
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise AssertionError(f"Unexpected status code: {response.status}")
        return json.loads(response.read().decode("utf-8"))


class ErnieConnectivityTest(unittest.TestCase):
    def test_ernie_api(self) -> None:
        api_key = os.environ.get("BAIDU_API_KEY", "").strip()
        if not api_key:
            self.skipTest("BAIDU_API_KEY is not configured; skipping live API check")

        try:
            result = request_ernie(api_key)
        except urllib.error.HTTPError as error:
            self.fail(f"Baidu API returned HTTP {error.code}: {error.read().decode(errors='replace')}")
        except (urllib.error.URLError, TimeoutError) as error:
            self.fail(f"Unable to reach Baidu API: {error}")

        self.assertIsInstance(result, dict)
        self.assertIn("choices", result)


if __name__ == "__main__":
    unittest.main()
