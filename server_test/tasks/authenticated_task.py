from locust import TaskSet, task


class ChatTask(TaskSet):
    @task
    def chat(self):
        access_token = (
            self.user.access_token if hasattr(self.user, "access_token") else None
        )
        if access_token:
            self.client.post(
                "/api/v1/chatbot/chat",
                json={"message": "Hello"},
                headers={"Authorization": f"Bearer {access_token}"},
            )
        else:
            self.client.post(
                "/api/v1/chatbot/chat",
                json={"message": "Hello"},
            )
