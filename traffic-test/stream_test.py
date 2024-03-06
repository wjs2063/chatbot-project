from locust import task, FastHttpUser


class MyUser(FastHttpUser):
    @task
    def index(self):
        url = "http://localhost:50000/api/v1/streaming/Rhythm%20and%20Blues%20Revue_1955'"
        response = self.client.get("http://localhost:50000/api/v1/streaming/Rhythm%20and%20Blues%20Revue_1955",
                                   headers={'range': '1-1000'})
