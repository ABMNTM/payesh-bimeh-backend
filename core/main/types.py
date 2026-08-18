from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "مرد"
    FEMALE = "F", "زن"


class RelationshipType(models.TextChoices):
    FATHER = "F", "پدر"
    MOTHER = "M", "مادر"
    CHILD = "C", "فرزند"
    SPOUSE = "S", "همسر"


class SubsidyRateType(models.TextChoices):
    HIRED = "H", "استخدام شده"
    FATHER = "F", "پدر"
    MOTHER = "M", "مادر"
    CHILD = "C", "فرزند"
    SPOUSE = "S", "همسر"


class EnrollmentStatus(models.TextChoices):
    DRAFT = "D", "پیش نویس"
    PENDING = "P", "در انتظار پرداخت"
    SUBMITTED = "S", "ارسال شده"
    CONFIRMED = "C", "تایید شده"
