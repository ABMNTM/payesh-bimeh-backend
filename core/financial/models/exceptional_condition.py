from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django_jalali.db import models as jmodels

import json


class ExceptionalCondition(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")

    rate_rule = models.ForeignKey(
        "financial.CostRateRule",
        models.CASCADE,
        related_name="exceptions",
        verbose_name="قانون"
    )

    condition = models.JSONField(help_text="این فیلد از استاندارد JsonLogic استفاده می کند.")

    priority = models.PositiveSmallIntegerField(default=0, verbose_name="اولویت")

    new_organ_share = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0, "حداقل درصد یارانه، صفر درصد است."),
            MaxValueValidator(100, "حداکثر درصد یارانه، 100 درصد است."),
        ],
        verbose_name="درصد سهم سازمان (یارانه)",
    )

    is_active = models.BooleanField(default=False, verbose_name="فعال؟")

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "شرط استثنایی"
        verbose_name_plural = "شروط استثنایی"
