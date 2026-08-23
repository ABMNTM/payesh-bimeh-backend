from django.db import models


class EmploymentType(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "نوع استخدام"
        verbose_name_plural = "انواع استخدام"
