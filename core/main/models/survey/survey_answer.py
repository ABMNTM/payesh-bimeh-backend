from django.db import models


class SurveyAnswer(models.Model):
    enrollment = models.ForeignKey(
        "main.Enrollment",
        models.CASCADE,
        related_name="answers",
        verbose_name="ثبت نام بیمه",
    )
    question = models.ForeignKey(
        "main.SurveyQuestion",
        models.CASCADE,
        related_name="answers",
        verbose_name="سوال"
    )
    anschoice = models.ForeignKey(
        "main.SurveyAnschoice",
        models.CASCADE,
        related_name="answers",
        verbose_name="گزینه"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "پاسخ نظرسنجی"
        verbose_name_plural = "پاسخ های نظرسنجی"
        constraints = (
            models.UniqueConstraint(fields=["enrollment", "question"], name="survey_answer_unq"),
        )
