from django.db import models


class SurveyQuestion(models.Model):
    content = models.CharField(max_length=1024, verbose_name="متن سوال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    class Meta:
        verbose_name = "سوال نظرسنجی"
        verbose_name_plural = "سوالات نظرسنجی"

    def __str__(self):
        return self.content[:20]
