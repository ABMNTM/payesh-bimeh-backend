from django.contrib.auth.models import UserManager as DjUserManager

from django.apps import apps

from main.models.employment_type import EmploymentType


class UserManager(DjUserManager):
    def create_superuser(self, national_code, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        User = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)

        awesome_employment_type = EmploymentType.objects.first()
        if not awesome_employment_type:
            raise EmploymentType.DoesNotExist

        email = self.normalize_email(email)

        user = User(
            national_code=national_code,
            employment_type=awesome_employment_type,
            email=email,
            **extra_fields
        )
        user.set_password(password)

        user.save()
