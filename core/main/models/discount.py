from django.db import models

from django.core.validators import MaxValueValidator

from accounts.models import User


class Discount(models.Model):
    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف ها"

    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(100, "درصد تخفیف باید بین 0 و 100 باشد."),
        ],
        verbose_name="درصد تخفیف",
    )

    type = models.CharField(
        max_length=1,
        choices=User.EmploymentType.choices,
        unique=True,
        verbose_name="نوع تخفیف",
    )
