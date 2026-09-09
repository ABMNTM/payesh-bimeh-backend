from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from accounts.models import User
from core.settings import ORGANIZATION_SERVICE_MAX_YEAR


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    پنل مدیریت کاربران سیستم
    """

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    list_display = (
        "person_display",
        "personnel_code",
        "employment_type__title",
        "employment_status",
        "is_active",
        "is_staff",
        "last_login",
    )

    list_display_links = ("person_display",)

    list_filter = (
        "employment_type",
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    search_fields = (
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
                    "personnel_code",
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
                    "birth_year",
                    "birth_month",
                    "birth_day",
                    "birth_place",
                    "bc_issuance_place",
                    "gender",
                ),
            },
        ),
        (
            "اطلاعات استخدامی",
            {
                "fields": (
                    (
                        "employment_type",
                        "organization_enter_year",
                        "organizational_unit",
                        "veteran_status",
                    ),
                    (
                        "phone_number",
                        "landline_number",
                        "address",
                        "postal_code",
                        "post_title",
                        "education_certificate",
                    ),
                    (
                        "account_number",
                        "iba_number",
                        "card_number",
                    ),
                    (
                        "description",
                        "extra_text_5",
                        "extra_text_6",
                        "extra_text_7",
                        "extra_text_8",
                        "extra_text_9",
                    ),
                    (
                        "available_services",
                        "insured_computer_code"
                    )
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
                    "changes_count",
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
                    "personnel_code",
                    "employment_type",
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
                        "organization_enter_year",
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
        from jdatetime import date

        if not obj.organization_enter_year:
            return format_html('<span style="color:#d3dcf9;">داده یافت نشد</span>')

        current_year = date.today().year
        end_year = obj.organization_enter_year + ORGANIZATION_SERVICE_MAX_YEAR

        if current_year >= end_year:
            return format_html('<span style="color:#d32f2f;">پایان یافته</span>')

        return format_html('<span style="color:#15803d;">فعال</span>')
    # ------------------------------------------------------------------
    # Queryset
    # ------------------------------------------------------------------

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("person", "employment_type")
