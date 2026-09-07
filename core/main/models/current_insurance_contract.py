from django.db import models


class CurrentInsuranceContract(models.Model):
    contract = models.ForeignKey(
        "main.InsuranceContract",
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="رکورد کنونی",
    )

    @classmethod
    def current(cls):
        return cls.objects.first()
