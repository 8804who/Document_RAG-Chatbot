from locust import TaskSet, task


class PublicTask(TaskSet):
    @task
    def index(self):
        self.client.get("/health")