from django.db import models
from django_jalali.db import models as jmodels


class EmploymentType(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "نوع استخدام"
        verbose_name_plural = "انواع استخدام"
