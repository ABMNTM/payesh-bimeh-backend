from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.types import EmploymentType
from main.types import SubsidyRateType


class CostRateRule(models.Model):
    contract = models.ForeignKey(
        "main.InsuranceContract",
        models.CASCADE,
        related_name="rate_rules",
        verbose_name="قرارداد بیمه سالانه",
    )

    employment_type = models.CharField(
        max_length=1,
        choices=EmploymentType.choices,
        verbose_name="نوع استخدام",
    )

    cost_type = models.CharField(
        max_length=1,
        choices=SubsidyRateType.choices,
        verbose_name="نوع رابطه برای محاسبه قیمت",
    )

    subsidy_percent = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0, "حداقل درصد یارانه، صفر درصد است."),
            MaxValueValidator(100, "حداکثر درصد یارانه، 100 درصد است."),
        ],
        verbose_name="درصد تخفیف یارانه",
    )

    base_premium_cost = models.PositiveBigIntegerField(
        default=0,
        verbose_name="هزینه پایه بابت بیمه",
    )

    class Meta:
        verbose_name = "قانون هزینه و یارانه بیمه"
        verbose_name_plural = "قوانین هزینه و یارانه بیمه"

    def __str__(self):
        return f"یارانه <{self.id}>"
