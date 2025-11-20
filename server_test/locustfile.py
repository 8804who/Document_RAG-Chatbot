from locust import HttpUser, task, between, TaskSet


class MainBehavior(TaskSet):
    @task
    def index(self):
        self.client.get("/health")


class LocustUser(HttpUser):
    host = "http://localhost:10004"
    tasks = [MainBehavior]
    wait_time = between(1, 4)
