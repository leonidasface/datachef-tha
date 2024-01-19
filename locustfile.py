# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def get_selector(self):
        self.client.get("/1")

    @task
    def post_selector(self):
        self.client.post("/1")