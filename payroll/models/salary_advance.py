from django.db import models
from core.models import Base

class SalaryAdvance(Base):
    employee = None
    amount = None
    to_pay = None

    start_dt = None
    end_dt = None