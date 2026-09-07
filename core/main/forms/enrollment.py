from django import forms
from common.utils.forms import BootstrapReadOnlyModelForm

from main.models import Enrollment


class EnrollmentCreateForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ("offer", "covered_members")
