from locust import HttpUser, between

from auth.google_oauth import get_google_access_token
from tasks.authenticated_task import ChatTask


class GoogleOAuthUser(HttpUser):
    wait_time = between(20, 60)
    access_token: str | None = None

    def on_start(self):
        self.access_token = get_google_access_token()

    tasks = [ChatTask]
