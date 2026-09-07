from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels

from main.types import Gender, RelationshipType


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

    created_at = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "رابطه خانوادگی"
        verbose_name_plural = "روابط خانوادگی"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "person",
                    "related_person",
                ],
                name="unique_family_relationship",
            ),
            models.CheckConstraint(
                condition=~Q(person=models.F("related_person")),
                name="person_cannot_be_related_to_itself",
            ),
        ]

        indexes = [
            models.Index(
                fields=["person", "relationship_type"]
            ),
            models.Index(
                fields=["related_person", "relationship_type"]
            ),
        ]

    INVERSE_RELATIONSHIPS = {
        RelationshipType.FATHER: RelationshipType.CHILD,
        RelationshipType.MOTHER: RelationshipType.CHILD,
        RelationshipType.SPOUSE: RelationshipType.SPOUSE
    }

    def get_inverse_relationship_type(self):
        if self.relationship_type == RelationshipType.CHILD:
            if self.person.gender == Gender.MALE:
                return RelationshipType.FATHER
            else:
                return RelationshipType.MOTHER
        return self.INVERSE_RELATIONSHIPS.get(
            self.relationship_type
        )

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)

        inverse_relationship_type = self.get_inverse_relationship_type()

        if not inverse_relationship_type:
            return

        FamilyRelationship.objects.get_or_create(
            person=self.related_person,
            related_person=self.person,
            defaults={
                "relationship_type": inverse_relationship_type,
            },
        )

    def clean(self):
        errors = {}

        if self.person_id == self.related_person_id:
            errors["related_person"] = (
                "یک فرد نمی‌تواند با خودش رابطه داشته باشد."
            )

        if not self.person_id or not self.related_person_id:
            if errors:
                raise ValidationError(errors)
            return

        person = self.person
        related = self.related_person

        # -----------------------------------------------------
        # پدر
        # -----------------------------------------------------

        if self.relationship_type == RelationshipType.FATHER:
            if person.gender != Gender.MALE:
                errors["person"] = (
                    "فردی که نقش پدر دارد باید مرد باشد."
                )

        # -----------------------------------------------------
        # مادر
        # -----------------------------------------------------

        elif self.relationship_type == RelationshipType.MOTHER:
            if person.gender != Gender.FEMALE:
                errors["person"] = (
                    "فردی که نقش مادر دارد باید زن باشد."
                )

        # -----------------------------------------------------
        # همسر
        # -----------------------------------------------------

        elif self.relationship_type == RelationshipType.SPOUSE:

            if person.gender == related.gender:
                errors["related_person"] = (
                    "رابطه همسر فقط بین زن و مرد مجاز است."
                )

            max_spouses = {
                Gender.MALE: 4,
                Gender.FEMALE: 1,
            }

            person_limit = max_spouses.get(person.gender)
            related_limit = max_spouses.get(related.gender)

            if person_limit is not None:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=person,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= person_limit:
                    errors["person"] = (
                        f"هر فرد حداکثر می‌تواند "
                        f"{person_limit} همسر داشته باشد."
                    )

            if related_limit is not None:
                spouse_count = (
                    FamilyRelationship.objects.filter(
                        person=related,
                        relationship_type=RelationshipType.SPOUSE,
                    )
                    .exclude(pk=self.pk)
                    .count()
                )

                if spouse_count >= related_limit:
                    errors["related_person"] = (
                        f"هر فرد حداکثر می‌تواند "
                        f"{related_limit} همسر داشته باشد."
                    )

        if errors:
            raise ValidationError(errors)
