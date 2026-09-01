from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django_jalali.db import models as jmodels

from main.types import SubsidyRateType


class CostRateRule(models.Model):
    offer = models.ForeignKey(
        "main.InsuranceOffer",
        models.CASCADE,
        related_name="rate_rules",
        verbose_name="پیشنهاد بیمه سالانه",
    )

    employment_type = models.ForeignKey(
        "main.EmploymentType",
        models.CASCADE,
        verbose_name="نوع استخدام",
    )

    cost_type = models.CharField(
        max_length=1,
        choices=SubsidyRateType.choices,
        verbose_name="نوع رابطه برای محاسبه قیمت",
    )

    organ_share_percent = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0, "حداقل درصد یارانه، صفر درصد است."),
            MaxValueValidator(100, "حداکثر درصد یارانه، 100 درصد است."),
        ],
        verbose_name="درصد سهم سازمان (یارانه)",
    )

    base_premium_cost = models.PositiveBigIntegerField(
        default=0,
        verbose_name="هزینه پایه بیمه",
    )

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "قانون هزینه و یارانه بیمه"
        verbose_name_plural = "قوانین هزینه و یارانه بیمه"

    def __str__(self):
        return f"یارانه <{self.id}>"
