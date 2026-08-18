from django.db import models

from main.types import EnrollmentStatus


class Enrollment(models.Model):
    status = models.CharField(
        max_length=1,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.DRAFT,
        verbose_name="وضعیت",
    )

    guardian = models.ForeignKey(
        "accounts.User",
        models.CASCADE,
        related_name="enrollments",
        verbose_name="کاربر",
    )

    contract = models.ForeignKey(
        "main.InsuranceContract",
        models.CASCADE,
        related_name="enrollments",
        verbose_name="قرارداد بیمه سالانه",
    )

    terms_accepted = models.BooleanField(
        default=False,
        verbose_name="تایید مطالعه قرارداد",
    )

    terms_accepted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان تایید قرارداد",
    )

    covered_members = models.ManyToManyField(
        "main.Person", related_name="enrollments", verbose_name="افراد تحت پوشش"
    )

    class Meta:
        verbose_name = "ثبت نام سالانه سرپرست"
        verbose_name_plural = "ثبت نام های سالانه سرپرست ها"
