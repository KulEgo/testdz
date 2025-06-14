from locust import HttpUser, task

class ShortistUser(HttpUser):
    @task
    def shorten(self):
        self.client.post("/api/shorten", json={"target_url": "https://example.com"})
