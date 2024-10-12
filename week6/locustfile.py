from locust import HttpUser, task, between

class User(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_index(self):
        self.client.get('/')
        self.client.get('/style.css')
        self.client.get('/main.js')
        self.client.get('/image.jpg')


