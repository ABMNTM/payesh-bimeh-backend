from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from core.main.types import Gender, RelationshipType


class FamilyRelationship(models.Model):
    person = models.ForeignKey(
        "main.Person",
        on_delete=models.CASCADE,
        related_name="relationships",
        verbose_name="فرد",
    )

    related_person = models.ForeignKey(
        "main.Person",
        on_delete=models.CASCADE,
        related_name="related_to",
        verbose_name="فرد مرتبط",
    )

    relationship_type = models.CharField(
        max_length=1,
        choices=RelationshipType.choices,
        verbose_name="نوع رابطه",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "رابطه خانوادگی"
        verbose_name_plural = "روابط خانوادگی"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "person",
                    "related_person",
                    "relationship_type",
                ],
                name="unique_family_relationship",
            ),
            models.CheckConstraint(
                condition=~Q(person=models.F("related_person")),
                name="person_cannot_be_related_to_itself",
            ),
        ]

        indexes = [
            models.Index(fields=["person", "relationship_type"]),
            models.Index(fields=["related_person", "relationship_type"]),
        ]

    def clean(self):
        errors = {}

        if self.person_id == self.related_person_id:
            errors["related_person"] = "یک فرد نمی‌تواند با خودش رابطه داشته باشد."

        if not self.person_id or not self.related_person_id:
            if errors:
                raise ValidationError(errors)
            return

        person = self.person
        related = self.related_person

        # --------------------------------------------------------------
        # کنترل رابطه پدر/مادر
        # --------------------------------------------------------------

        if self.relationship_type == RelationshipType.FATHER:
            if person.gender != Gender.MALE:
                errors["person"] = "فردی که نقش پدر دارد باید مرد باشد."

        elif self.relationship_type == RelationshipType.MOTHER:
            if person.gender != Gender.FEMALE:
                errors["person"] = "فردی که نقش مادر دارد باید زن باشد."

        # --------------------------------------------------------------
        # کنترل رابطه همسر
        # --------------------------------------------------------------

        elif self.relationship_type == RelationshipType.SPOUSE:

            if person.gender == related.gender:
                errors["related_person"] = "رابطه همسر فقط بین زن و مرد مجاز است."

            # اگر فرد مرد باشد، حداکثر 4 همسر
            if person.gender == Gender.MALE:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=person,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= 4:
                    errors["person"] = "هر مرد حداکثر می‌تواند ۴ همسر داشته باشد."

            # اگر فرد زن باشد، حداکثر یک همسر
            elif person.gender == Gender.FEMALE:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=person,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= 1:
                    errors["person"] = "هر زن حداکثر می‌تواند یک همسر داشته باشد."

            # کنترل سمت مقابل نیز لازم است.
            if related.gender == Gender.MALE:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=related,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= 4:
                    errors["related_person"] = (
                        "هر مرد حداکثر می‌تواند ۴ همسر داشته باشد."
                    )

            elif related.gender == Gender.FEMALE:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=related,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= 1:
                    errors["related_person"] = (
                        "هر زن حداکثر می‌تواند یک همسر داشته باشد."
                    )

        if errors:
            raise ValidationError(errors)
