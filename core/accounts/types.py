from django.db import models


class EmploymentType(models.TextChoices):
    RETIRED = "R", "بازنشسته"
    FACULTY = "F", "هیات علمی"
    EMPLOYEE = "E", "کارمند"
    COMPANY_EMPLOYEE = "C", "کارمند شرکتی"
