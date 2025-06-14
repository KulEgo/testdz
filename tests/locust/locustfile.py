from locust import HttpUser, task, between

class ShortistUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def shorten(self):
        response = self.client.post("/api/shorten", json={"target_url": "https://example.com"})
        if response.status_code == 200:
            short_code = response.json().get("short_code")
            if short_code:
                self.client.get(f"/{short_code}", catch_response=True)
