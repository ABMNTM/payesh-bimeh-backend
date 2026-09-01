from django.db import models
from django_jalali.db import models as jmodels

from main.types import EnrollmentStatus


class Enrollment(models.Model):
    status = models.CharField(
        max_length=1,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.PENDING,
        verbose_name="وضعیت",
    )

    guardian = models.ForeignKey(
        "accounts.User",
        models.CASCADE,
        related_name="enrollments",
        verbose_name="کاربر",
    )

    offer = models.ForeignKey(
        "main.InsuranceOffer",
        models.CASCADE,
        related_name="enrollments",
        verbose_name="پیشنهاد بیمه سالانه",
    )

    covered_members = models.ManyToManyField(
        "main.Person", related_name="enrollments", verbose_name="افراد تحت پوشش"
    )

    enrolled_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ثبت نام")

    class Meta:
        verbose_name = "ثبت نام سالانه سرپرست"
        verbose_name_plural = "ثبت نام های سالانه سرپرست ها"
