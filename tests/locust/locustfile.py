from locust import HttpUser, task, between

class ShortistUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_short_link(self):
        url = "https://example.com"
        self.client.post("/shorten", json={"url": url})

    @task
    def redirect_short_link(self):
        # Можно использовать заранее известный short_code или создать новый
        short_code = "abc123"
        self.client.get(f"/{short_code}")
