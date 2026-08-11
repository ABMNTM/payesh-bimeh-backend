from django.db import models

from accounts.models import User

from common.utils.fields import NationalCodeField


class FamilyMember(models.Model):
    class Meta:
        verbose_name = "عضو خانواده"
        verbose_name_plural = "اعضای خانواده"
        ordering = ["last_name", "first_name"]

    class FamilyRole(models.TextChoices):
        HUSBAND = "H", "همسر"
        CHILD = "C", "فرزند"
        FATHER = "F", "پدر"
        MOTHER = "M", "مادر"
        SISTER = "S", "خواهر"
        BROTHER = "B", "برادر"

    insured = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="family_members",
        verbose_name="بیمه‌شده اصلی",
    )

    insurance_period = models.ForeignKey(
        "main.InsurancePeriod",
        models.CASCADE,
        related_name="insured_family_members",
        verbose_name="دوره بیمه تکمیلی"
    )

    first_name = models.CharField(
        max_length=255,
        verbose_name="نام",
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name="نام خانوادگی",
    )

    national_code = NationalCodeField()

    father_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="نام پدر",
    )

    birth_date = models.DateField(
        verbose_name="تاریخ تولد",
    )

    gender = models.CharField(
        max_length=1,
        choices=User.Gender.choices,
        verbose_name="جنسیت",
    )

    birth_certificate_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره شناسنامه",
    )

    family_role = models.CharField(
        max_length=1,
        choices=FamilyRole.choices,
        verbose_name="نقش در خانواده",
    )

    phone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name="شماره موبایل",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="توضیحات",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ آخرین ویرایش",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
