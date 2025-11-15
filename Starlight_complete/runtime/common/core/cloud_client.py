import os
import uuid
import json
import urllib.request
import urllib.error


class CloudClient:
    """
    HTTP client for Starlight cloud.
    Provides embedding, reasoning, and health checks.
    """

    def __init__(self, api_url=None):
        self.api_url = api_url or os.environ.get("STARLIGHT_CLOUD_URL", "http://localhost:8000")

    def health_check(self):
        """
        Check if cloud is reachable.
        """
        try:
            req = urllib.request.Request(f"{self.api_url}/health", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False

    def embed(self, text):
        """
        Get embedding vector for text.
        """
        request_id = str(uuid.uuid4())
        payload = {"text": text, "request_id": request_id}
        result = self._post("/embed", payload)
        return result.get("embedding", [])

    def reason(self, context_bundle):
        """
        Send context bundle to cloud for reasoning.
        Returns generated response text.
        """
        request_id = str(uuid.uuid4())
        payload = {
            "context": context_bundle,
            "request_id": request_id
        }
        result = self._post("/reason", payload)
        return result.get("response", "")

    def _post(self, endpoint, payload):
        """
        Internal POST helper.
        """
        url = f"{self.api_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")
                result = json.loads(body)
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            return {"error": f"HTTP {e.code}: {error_body}"}
        except Exception as e:
            return {"error": str(e)}


# Singleton
_client = None


def get_cloud_client():
    global _client
    if _client is None:
        _client = CloudClient()
    return _client
