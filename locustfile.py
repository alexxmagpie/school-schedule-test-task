from locust import HttpUser, task


class ScheduleLocustTask(HttpUser):
    @task
    def get_all_schedule(self):
        self.client.get('/api/schedule')
