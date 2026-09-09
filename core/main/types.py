from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "مرد"
    FEMALE = "F", "زن"


class RelationshipType(models.TextChoices):
    FATHER = "F", "پدر"
    MOTHER = "M", "مادر"
    S_CHILD = "C", "فرزند پسر"
    D_CHILD = "D", "فرزند دختر"
    SPOUSE = "S", "همسر"


class SubsidyRateType(models.TextChoices):
    HIRED = "H", "استخدام شده"
    FATHER = "F", "پدر"
    MOTHER = "M", "مادر"
    CHILD = "C", "فرزند"
    SPOUSE = "S", "همسر"


class EnrollmentStatus(models.TextChoices):
    PENDING = "P", "در انتظار پرداخت"
    SUBMITTED = "S", "ارسال شده"
    CONFIRMED = "C", "تایید شده"


class VeteranStatus(models.TextChoices):
    VETERAN = "V", "ایثارگر"
    DISABLED = "D", "جانباز"
    MARTYR_SPOUSE = "S", "همسر شهید"
    MARTYR_CHILD = "C", "فرزند شهید"
    FORMER_POW  = "F", "آزاده"
    NONE = "N", "ندارد"
