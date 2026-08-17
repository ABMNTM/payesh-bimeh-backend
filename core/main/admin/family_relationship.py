from django.contrib import admin

from main.models import FamilyRelationship


@admin.register(FamilyRelationship)
class FamilyRelationshipAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "person",
        "related_person",
        "relationship_type",
    )
