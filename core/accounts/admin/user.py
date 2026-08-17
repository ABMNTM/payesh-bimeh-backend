from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from accounts.models import User
from main.models import Person


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    پنل مدیریت کاربران سیستم
    """

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    list_display = (
        "username",
        "person_display",
        "personnel_code",
        "employment_type",
        "employment_status",
        "is_active",
        "is_staff",
        "last_login",
    )

    list_display_links = (
        "username",
        "person_display",
    )

    list_filter = (
        "employment_type",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "person__first_name",
        "person__last_name",
        "person__national_code",
        "personnel_code",
    )

    ordering = (
        "person__last_name",
        "person__first_name",
    )

    date_hierarchy = "date_joined"

    list_per_page = 30

    # جلوگیری از query اضافه برای Person
    list_select_related = ("person",)

    # به جای select معمولی با جستجو
    autocomplete_fields = ("person",)

    # ------------------------------------------------------------------
    # Fieldsets
    # ------------------------------------------------------------------

    fieldsets = (
        (
            "اطلاعات حساب کاربری",
            {
                "fields": (
                    "username",
                    "password",
                ),
            },
        ),
        (
            "اطلاعات شخص",
            {
                "fields": (
                    "person",
                    "email",
                ),
            },
        ),
        (
            "اطلاعات استخدامی",
            {
                "fields": (
                    "employment_type",
                    "personnel_code",
                    (
                        "employment_start_date",
                        "employment_end_date",
                    ),
                ),
            },
        ),
        (
            "دسترسی‌ها",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "اطلاعات سیستمی",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # ------------------------------------------------------------------
    # Add form
    # ------------------------------------------------------------------

    add_fieldsets = (
        (
            "ایجاد کاربر",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "اطلاعات شخص",
            {
                "fields": (
                    "person",
                    "email",
                ),
            },
        ),
        (
            "اطلاعات استخدامی",
            {
                "fields": (
                    "employment_type",
                    "personnel_code",
                    (
                        "employment_start_date",
                        "employment_end_date",
                    ),
                ),
            },
        ),
        (
            "دسترسی‌ها",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )

    # ------------------------------------------------------------------
    # Display methods
    # ------------------------------------------------------------------

    @admin.display(
        description="شخص",
        ordering="person__last_name",
    )
    def person_display(self, obj):
        if not obj.person:
            return format_html('<span style="color:#999;">بدون شخص</span>')

        return str(obj.person)

    @admin.display(
        description="وضعیت استخدام",
    )
    def employment_status(self, obj):
        if (
            obj.employment_end_date
            and obj.employment_end_date < obj.employment_start_date
            if obj.employment_start_date
            else False
        ):
            return format_html('<span style="color:#d32f2f;">نامعتبر</span>')

        if obj.employment_end_date:
            return format_html('<span style="color:#d97706;">پایان یافته</span>')

        return format_html('<span style="color:#15803d;">فعال</span>')

    # ------------------------------------------------------------------
    # Queryset
    # ------------------------------------------------------------------

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person")
