from domain.contracts.repositories.activity_repository import ActivityRepository
from infrastructure.external_services.employee_activity_service import EmployeeActivityService

class EmployeeActivityRepositoryImpl(ActivityRepository):
    def __init__(self, employee_activity_service: EmployeeActivityService):
        self.employee_activity_service = employee_activity_service

    def get_activities_for_employee(self, employee_id):
        activities_data = self.employee_activity_service.get_employee_activities(employee_id)
        return activities_data
