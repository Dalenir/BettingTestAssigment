from main import app
from fastapi.testclient import TestClient

test_client = TestClient(app, backend="asyncio")
