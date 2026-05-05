import base64
import json
import os

import httpx

ENDURAIN_URL = os.environ["ENDURAIN_URL"].rstrip("/")
ENDURAIN_USERNAME = os.environ["ENDURAIN_USERNAME"]
ENDURAIN_PASSWORD = os.environ["ENDURAIN_PASSWORD"]


def _decode_user_id_from_jwt(token: str) -> int:
    payload_part = token.split(".")[1]
    padding = 4 - len(payload_part) % 4
    if padding != 4:
        payload_part += "=" * padding
    payload = json.loads(base64.urlsafe_b64decode(payload_part))
    return int(payload["sub"])


class EndurainClient:
    def __init__(self):
        self._access_token: str | None = None
        self._user_id: int | None = None

    def _login(self):
        response = httpx.post(
            f"{ENDURAIN_URL}/api/v1/auth/login",
            data={
                "username": ENDURAIN_USERNAME,
                "password": ENDURAIN_PASSWORD,
                "grant_type": "password",
                "scope": "activities:read health:read profile",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded", "X-Client-Type": "web"},
            verify=False,
        )
        import sys
        print(f"LOGIN STATUS: {response.status_code}", file=sys.stderr)
        print(f"LOGIN BODY: {response.text[:500]}", file=sys.stderr)
        response.raise_for_status()
        data = response.json()
        self._access_token = data.get("access_token")
        print(f"ACCESS TOKEN PRESENT: {bool(self._access_token)}", file=sys.stderr)
        if self._access_token:
            self._user_id = _decode_user_id_from_jwt(self._access_token)

    def _headers(self) -> dict:
        if not self._access_token:
            self._login()
        return {"Authorization": f"Bearer {self._access_token}"}

    def request(self, method: str, path: str, **kwargs) -> dict | list | None:
        url = f"{ENDURAIN_URL}/api/v1{path}"
        response = httpx.request(
            method, url, headers=self._headers(), verify=False, **kwargs
        )
        if response.status_code == 401:
            self._access_token = None
            self._login()
            response = httpx.request(
                method, url, headers=self._headers(), verify=False, **kwargs
            )
        response.raise_for_status()
        return response.json()

    @property
    def user_id(self) -> int:
        if self._user_id is None:
            self._login()
        return self._user_id


# Shared singleton used by all tools
client = EndurainClient()
