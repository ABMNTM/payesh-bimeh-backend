from django.db import models
from django_jalali.db import models as jmodels

from financial.models.payment import Payment


class Transaction(models.Model):
    authority = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="شناسه نشست پرداخت",
    )

    reference_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="شناسه مرجع پرداخت",
    )

    amount = models.PositiveBigIntegerField(
        verbose_name="مبلغ پرداختی",
    )

    enrollment = models.ForeignKey(
        "main.Enrollment",
        models.CASCADE,
        related_name="transactions",
        verbose_name="ثبت نام بیمه",
    )

    success = models.BooleanField(
        default=False, verbose_name="موفقیت آمیز؟"
    )

    paid_at = jmodels.jDateTimeField(null=True, blank=True, verbose_name="تاریخ پرداخت")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    def __str__(self):
        return self.authority

    class Meta:
        verbose_name = "تراکنش بانکی"
        verbose_name_plural = "تراکنش های بانکی"
    

    def payment_request(self):
        response = Payment(self.amount).request()
        self.authority = response.get("authority")

        self.save()
        return self.authority

    def payment_verify(self):
        response = Payment(self.amount).verify()
        if success:= response.get("success"):
            self.success = True
            self.reference_id = response.get("reference_id")
            self.paid_at = response.get("paid_at")
            self.save()
        return success
