from django.core.validators import RegexValidator
from django.db import models


class NationalCodeField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r"^\d{10}$",
            message="کد ملی باید شامل ۱۰ رقم باشد.",
        )
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 10)
        kwargs.setdefault("db_index", True)
        kwargs.setdefault("verbose_name", "کد ملی")

        super().__init__(*args, **kwargs)
