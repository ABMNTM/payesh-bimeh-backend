from django import forms
from captcha.fields import CaptchaField


class CaptchaForm(forms.Form):
    captcha = CaptchaField(
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["captcha"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "کد تصویر را وارد کنید",
            "autocomplete": "off",
        })
