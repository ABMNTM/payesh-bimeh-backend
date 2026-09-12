from django.contrib import admin

from main.models import SurveyAnswer


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "enrollment",
        "question",
        "anschoice",
        "created_at",
    )
