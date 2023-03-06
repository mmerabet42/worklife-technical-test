import sqlalchemy as sa
from .base import BaseModel
from .vacation import VacationModel

class EmployeeModel(BaseModel):
	__tablename__ = "employee"

	first_name = sa.Column(sa.String, nullable=False)
	last_name = sa.Column(sa.String, nullable=False)
	vacations = sa.orm.relationship(VacationModel.__name__, backref="employee")
    
	# def __str__(self):
		# return f"<Employee #{self.id}> {self.first_name} - {self.last_name}"
