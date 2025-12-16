from locust import HttpUser, between

from tasks.authenticated_task import ChatTask


class UnauthenticatedUser(HttpUser):
    wait_time = between(20, 60)
    tasks = [ChatTask]
