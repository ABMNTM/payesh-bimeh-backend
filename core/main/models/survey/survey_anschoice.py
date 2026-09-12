from django.db import models


class SurveyAnschoice(models.Model):
    content = models.CharField(max_length=1024, verbose_name="متن گزینه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "گزینه نظرسنجی"
        verbose_name_plural = "گزینه های نظرسنجی"

    def __str__(self):
        return self.content[:10]
