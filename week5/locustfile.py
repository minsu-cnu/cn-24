from locust import HttpUser, task

class User(HttpUser):
    @task
    def get_index(self):
        self.client.get('/')
        self.client.get('/style.css')
        self.client.get('/main.js')
        self.client.get('/image.jpg')


