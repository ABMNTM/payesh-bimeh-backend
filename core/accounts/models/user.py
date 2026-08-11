from django.db import models
from django.contrib.auth.models import AbstractUser
from common.utils.fields import NationalCodeField


class User(AbstractUser):
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    class Gender(models.TextChoices):
        MALE = "M", "آقا"
        FEMALE = "F", "خانم"

    class EmploymentType(models.TextChoices):
        RETIRED = "R", "بازنشسته"
        FACULTY = "F", "هیأت علمی"
        EMPLOYEE = "E", "کارمند"
        CORPORATE = "C", "کارمند شرکتی"

    national_code = NationalCodeField()

    phone_number = models.CharField(
        max_length=14, verbose_name="شماره همراه"
    )

    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد")

    gender = models.CharField(
        max_length=1, null=True, blank=True, choices=Gender.choices, verbose_name="جنسیت"
    )

    employment_type = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=EmploymentType.choices,
        verbose_name="نوع کارمندی"
    )
