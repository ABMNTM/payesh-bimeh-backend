from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django_jalali.db import models as jmodels
import jdatetime

from main.types import EducationalCertificates, RelationshipType


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

    birth_date = jmodels.jDateField(
        verbose_name="تاریخ تولد",
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

    relation_type = models.CharField(
        max_length=1,
        null=True,
        blank=True,
        choices=RelationshipType.choices,
        verbose_name="نسبت با سرپرست"
    )

    tracking_code = models.CharField(
        max_length=45,
        verbose_name="کد رهگیری",
        editable=False,
    )

    educational_certificate = models.CharField(
        max_length=1, choices=EducationalCertificates.choices, verbose_name="آخرین مدرک تحصیلی"
    )

    edu_in_progress = models.BooleanField(default=True, verbose_name="در حال تحصیل؟")

    is_married = models.BooleanField(default=False, verbose_name="ازدواج کرده؟")

    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="زمان آخرین تغییرات")

    @property
    def age(self):
        reference_date = jdatetime.date.today()
        age = reference_date.year - self.birth_date.year
        if (reference_date.month, reference_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def clean(self):
        if self.is_household_head:
            if self.national_code != self.user.national_code:
                raise ValidationError("کدملی با کدملی ثبت شده مغایرت دارد.")

    class Meta:
        verbose_name = "فرد"
        verbose_name_plural = "افراد"

        constraints = [
            # یک فرد یا سرپرست خانوار است یا زیرمجموعه یک خانوار
            models.CheckConstraint(
                condition=(
                    Q(
                        is_household_head=True,
                        household__isnull=True,
                        relation_type__isnull=True,
                    )
                    | Q(
                        is_household_head=False,
                        household__isnull=False,
                        relation_type__isnull=False,
                    )
                ),
                name="valid_household_assignment",
            ),
        ]

        indexes = [
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
