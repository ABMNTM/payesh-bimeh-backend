from django.db import models
from django_jalali.db import models as jmodels

from core.storage import MediaStorage


class InsuranceContract(models.Model):
    contract_year = models.PositiveSmallIntegerField(
        verbose_name="سال قرارداد",
    )

    insurer_company = models.CharField(
        max_length=200,
        verbose_name="شرکت بیمه طرف قرارداد",
    )

    terms_file = models.FileField(
        storage=MediaStorage,
        upload_to="contracts/",
        verbose_name="فایل قرارداد بیمه",
    )

    start_date = jmodels.jDateField(
        verbose_name="تاریخ شروع پوشش",
    )

    end_date = jmodels.jDateField(
        verbose_name="تاریخ پایان پوشش",
    )

    created_at = jmodels.jDateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = jmodels.jDateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین ویرایش",
    )

    class Meta:
        verbose_name = "قرارداد بیمه"
        verbose_name_plural = "قراردادهای بیمه"

        constraints = [
            models.UniqueConstraint(
                fields=["contract_year"],
                name="unique_insurance_contract_year",
            ),
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="contract_end_after_start",
            ),
        ]

        ordering = ["-contract_year"]

    def __str__(self):
        return f"قرارداد بیمه {self.contract_year}"
