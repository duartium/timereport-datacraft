import requests

class EmployeeActivityService:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_employee_activities(self, employee_id):
        response = requests.get(f"{self.base_url}/activities/{employee_id}")
        response.raise_for_status()
        return response.json()