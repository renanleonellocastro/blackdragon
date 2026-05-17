"""Load test script for SC-006 (100 concurrent users).

Usage:
    pip install locust
    locust -f backend/tests/performance/load_test.py --host http://localhost:8000
"""
from locust import HttpUser, between, task


class BlackDragonUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self) -> None:
        resp = self.client.post("/api/auth/login", json={
            "email": "client@test.com",
            "password": "client123",
        })
        if resp.status_code == 200:
            self.token = resp.json().get("access_token", "")
        else:
            self.token = ""

    @property
    def auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def health_check(self) -> None:
        self.client.get("/api/health")

    @task(2)
    def list_projects(self) -> None:
        self.client.get("/api/projects", headers=self.auth_headers)

    @task(1)
    def list_blog(self) -> None:
        self.client.get("/api/blog")
