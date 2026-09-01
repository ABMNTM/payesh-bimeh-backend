from django.db import models

from django_jalali.db import models as jmodels


class InsuranceOffer(models.Model):
    contract = models.ForeignKey(
        "main.InsuranceContract",
        models.CASCADE,
        related_name="offers",
        verbose_name="قرارداد بیمه",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="عنوان",
    )

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "پیشنهاد بیمه (سطح بندی)"
        verbose_name_plural = "پیشنهادات بیمه (سطح بندی ها)"
