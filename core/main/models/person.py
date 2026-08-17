from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from main.types import Gender


class Person(models.Model):
    # ------------------------------------------------------------------
    # اطلاعات هویتی
    # ------------------------------------------------------------------

    first_name = models.CharField(
        max_length=100,
        verbose_name="نام",
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="نام خانوادگی",
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی",
    )

    birth_certificate_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره شناسنامه",
    )

    father_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام پدر",
    )

    mother_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نام مادر",
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تولد",
    )

    birth_place = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="محل تولد",
    )

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="جنسیت",
    )

    # ------------------------------------------------------------------
    # اطلاعات خانوار
    # ------------------------------------------------------------------

    is_household_head = models.BooleanField(
        default=False, verbose_name="سرپرست خانوار است؟"
    )

    household = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="household_members",
        verbose_name="سرپرست",
    )

    # ------------------------------------------------------------------
    # اطلاعات تکمیلی مورد استفاده در فرآیندهای بیمه
    # ------------------------------------------------------------------

    national_id_serial = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="سریال کارت ملی",
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره موبایل",
    )

    landline_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="شماره تلفن ثابت",
    )

    address = models.TextField(
        blank=True,
        verbose_name="نشانی",
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="کد پستی",
    )

    # ------------------------------------------------------------------
    # تاریخچه ثبت
    # ------------------------------------------------------------------

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "فرد"
        verbose_name_plural = "افراد"

        constraints = [
            # یک فرد یا سرپرست خانوار است یا زیرمجموعه یک خانوار
            models.CheckConstraint(
                condition=(
                    Q(is_household_head=True, household__isnull=True)
                    | Q(is_household_head=False, household__isnull=False)
                ),
                name="valid_household_assignment",
            ),
        ]

        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
