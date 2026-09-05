from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django_jalali.db import models as jmodels

from main.types import Gender, VeteranStatus


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

    birth_date = jmodels.jDateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تولد",
    )

    birth_year = models.PositiveSmallIntegerField(
        verbose_name="سال تولد"
    )

    birth_month = models.PositiveSmallIntegerField(
        verbose_name="ماه تولد"
    )

    birth_day = models.PositiveSmallIntegerField(
        verbose_name="روز تولد"
    )

    birth_place = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="محل تولد",
    )

    bc_issuance_place = models.CharField(
        max_length=255,
        verbose_name="محل صدور شناسنامه"
    )

    bc_issuance_province = models.CharField(
        max_length=255,
        verbose_name="استان محل صدور شناسنامه"
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

    deployed_unit = models.CharField(
        max_length=255,
        verbose_name="واحد مستقر"
    )

    organizational_unit = models.CharField(
        max_length=255,
        verbose_name="واحد سازمانی"
    )

    veteran_status = models.CharField(
        max_length=1,
        choices=VeteranStatus.choices,
        verbose_name="وضعیت ایثارگری"
    )

    account_number = models.CharField(
        max_length=20,
        verbose_name="شماره حساب"
    )

    iba_number = models.CharField(
        max_length=30,
        verbose_name="شماره شبا"
    )

    card_number = models.CharField(
        max_length=16,
        verbose_name="شماره کارت"
    )

    description = models.TextField(
        blank=True,
        verbose_name="توضیحات"
    )

    extra_text_5 = models.TextField(
        blank=True,
        verbose_name="متن اضافه 5"
    )

    extra_text_6 = models.TextField(
        blank=True,
        verbose_name="متن اضافه 6"
    )

    extra_text_7 = models.TextField(
        blank=True,
        verbose_name="متن اضافه 7"
    )

    extra_text_8 = models.TextField(
        blank=True,
        verbose_name="متن اضافه 8"
    )

    extra_text_9 = models.TextField(
        blank=True,
        verbose_name="متن اضافه 9"
    )

    post_title = models.CharField(
        max_length=255,
        verbose_name="عنوان پست"
    )

    tracking_code = models.CharField(
        max_length=45,
        verbose_name="کد رهگیری"
    )

    education_certificate = models.CharField(
        max_length=255,
        verbose_name="مدرک تحصیلی"
    )

    available_services = models.CharField(
        max_length=1024,
        verbose_name="خدمات قابل ارائه"
    )

    insured_computer_code = models.CharField(
        max_length=54,
        verbose_name="کد رایانه بیمه شده",
    )

    # ------------------------------------------------------------------
    # تاریخچه ثبت
    # ------------------------------------------------------------------

    changes_count = models.PositiveIntegerField(default=0, verbose_name="تعداد تغییرات")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان آخرین تغییرات")

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
