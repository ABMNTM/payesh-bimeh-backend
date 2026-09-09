from common.utils.forms import BootstrapModelForm

from accounts.models import User


class UserProfileForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['changes_count'].disabled = True

    class Meta:
        model = User
        exclude = (
            "id",
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "is_active",
            "person",
        )
