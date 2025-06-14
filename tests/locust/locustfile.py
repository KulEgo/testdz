from locust import HttpUser, task, between

class ShortistUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def shorten_link(self):
        self.client.post("/shorten", json={"url": "https://example.com"})

    @task(1)
    def redirect_link(self):
        # Тут желательно подставлять реальные короткие ссылки, для теста возьмем заглушку
        self.client.get("/abc123")
