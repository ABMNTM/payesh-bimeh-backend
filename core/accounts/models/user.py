from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from accounts.types import EmploymentType


class User(AbstractUser):
    person = models.OneToOneField(
        "main.Person",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="user",
    )

    employment_type = models.CharField(
        max_length=1,
        choices=EmploymentType.choices,
        verbose_name="نوع استخدام",
    )

    personnel_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="شماره پرسنلی",
    )

    employment_start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ شروع به کار",
    )

    employment_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ پایان کار",
    )

    def clean(self):
        errors = {}

        if not self.person.is_household_head:
            errors["person"] = "فرد باید سرپرست خانوار باشد."

        # تاریخ پایان نباید قبل از شروع باشد.
        if (
            self.employment_start_date
            and self.employment_end_date
            and self.employment_end_date < self.employment_start_date
        ):
            errors["employment_end_date"] = (
                "تاریخ پایان استخدام نمی‌تواند قبل از تاریخ شروع باشد."
            )

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.personnel_code
