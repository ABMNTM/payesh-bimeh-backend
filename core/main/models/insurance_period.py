from django.db import models


class InsurancePeriod(models.Model):
    class Meta:
        verbose_name = "دوره بیمه تکمیلی"
        verbose_name_plural = "دوره های بیمه تکمیلی"
        ordering = ["-start_date"]

    name = models.CharField(max_length=255, verbose_name="نام")

    start_date = models.DateField(verbose_name="تاریخ آغاز دوره")
    end_date = models.DateField(verbose_name="تاریخ پایان دوره")

    main_cost = models.PositiveBigIntegerField(verbose_name="هزینه اصلی (سرپرست خانوار)")
    family_member_cost = models.PositiveBigIntegerField(verbose_name="هزینه افراد تحت تکفل")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")
