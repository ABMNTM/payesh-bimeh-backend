from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels

from accounts.managers import UserManager
from main.types import Gender, VeteranStatus


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "personnel_code"

    person = models.OneToOneField(
        "main.Person",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="user",
    )

    employment_type = models.ForeignKey(
        "main.EmploymentType",
        models.CASCADE,
        related_name="hired_users",
        verbose_name="نوع استخدام",
    )

    personnel_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="شماره پرسنلی",
    )

    organization_enter_year = models.PositiveSmallIntegerField(
        verbose_name="سال ورود به سازمان",
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

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name="جنسیت",
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name="شماره موبایل",
    )

    landline_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="شماره تلفن ثابت",
    )

    address = models.TextField(
        blank=True,
        verbose_name="نشانی",
    )

    postal_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="کد پستی",
    )

    organizational_unit = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="واحد سازمانی"
    )

    veteran_status = models.CharField(
        max_length=1,
        choices=VeteranStatus.choices,
        verbose_name="وضعیت ایثارگری"
    )

    account_number = models.CharField(
        null=True,
        blank=True,
        max_length=20,
        verbose_name="شماره حساب"
    )

    iba_number = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name="شماره شبا"
    )

    card_number = models.CharField(
        max_length=16,
        null=True,
        blank=True,
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
        null=True,
        blank=True,
        verbose_name="عنوان پست"
    )

    education_certificate = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="مدرک تحصیلی"
    )

    available_services = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        verbose_name="خدمات قابل ارائه"
    )

    insured_computer_code = models.CharField(
        max_length=54,
        null=True,
        blank=True,
        verbose_name="کد رایانه بیمه شده",
    )

    # ------------------------------------------------------------------
    # تاریخچه ثبت
    # ------------------------------------------------------------------

    changes_count = models.PositiveIntegerField(default=0, verbose_name="تعداد تغییرات")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان آخرین تغییرات")

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.changes_count += 1
        return super().save(*args, **kwargs)

    def clean(self):
        errors = {}

        if not self.person.is_household_head:
            errors["person"] = "فرد باید سرپرست خانوار باشد."

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.personnel_code
