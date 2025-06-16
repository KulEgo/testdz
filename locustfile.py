from locust import HttpUser, task, between

class TaskUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def create_task(self):
        self.client.post(
            "/tasks/",
            json={
                "title": "Load Test Task",
                "description": "Created by Locust",
                "status": "pending",
                "priority": 1
            }
        )

    @task(1)
    def get_tasks(self):
        self.client.get("/tasks/")
