import os
import json
import unittest
from urllib import request, error

BASE_URL = os.environ.get("BASE_URL")

@unittest.skipUnless(BASE_URL, "Set BASE_URL environment variable to run these tests")
class AuthFormsTest(unittest.TestCase):
    def _make_request(self, path, payload):
        data = json.dumps(payload).encode()
        req = request.Request(f"{BASE_URL}{path}", data=data, headers={"Content-Type": "application/json"})
        try:
            with request.urlopen(req) as resp:
                body = resp.read().decode()
                return resp.getcode(), json.loads(body) if body else {}
        except error.HTTPError as exc:
            body = exc.read().decode()
            return exc.code, json.loads(body) if body else {}

    def test_registration(self):
        code, data = self._make_request("/register", {"username": "autotest", "password": "secret"})
        self.assertIn(code, (200, 201))
        self.assertEqual(data.get("username"), "autotest")

    def test_login(self):
        # Ensure user exists before login attempt
        self._make_request("/register", {"username": "autotest", "password": "secret"})
        code, data = self._make_request("/login", {"username": "autotest", "password": "secret"})
        self.assertEqual(code, 200)
        self.assertIn("token", data)


if __name__ == "__main__":
    unittest.main()
