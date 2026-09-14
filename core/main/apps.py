from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib import admin

        original_get_app_list = admin.site.get_app_list

        def get_app_list(request, app_label=None):
            app_list = original_get_app_list(request, app_label=app_label)
            app_list = [
                {
                    "name": "عملیات های ویژه",
                    "app_label": "reports",
                    "app_url": "#",
                    "has_module_perms": True,
                    "models": [
                        {
                            "name": "خروجی اکسل",
                            "object_name": "custom_report",
                            "admin_url": "/admin/report/",
                            "view_only": True,
                            "perms": {"view": True, "add": False, "change": False, "delete": False},
                        },
                        {
                            "name": "ورودی اکسل",
                            "object_name": "custom_report",
                            "admin_url": "/admin/import-excel/",
                            "view_only": True,
                            "perms": {"view": True, "add": False, "change": False, "delete": False},
                        },
                        {
                            "name": "ادغام دو فایل اکسل",
                            "object_name": "custom_report",
                            "admin_url": "/admin/merge-excel/",
                            "view_only": True,
                            "perms": {"view": True, "add": False, "change": False, "delete": False},
                        },
                    ],
                }
            ] + app_list

            return app_list

        admin.site.get_app_list = get_app_list
