from django import forms


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            # Input های معمولی
            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.URLInput,
                    forms.TelInput,
                )
            ):
                widget.attrs["class"] = "form-control"

            # Textarea
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("rows", 3)

            # Select
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"

            # Checkbox
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"

            # File
            elif isinstance(widget, forms.FileInput):
                widget.attrs["class"] = "form-control"

            # Date / DateTime
            elif isinstance(widget, (forms.DateInput, forms.DateTimeInput)):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("type", "date")

            # سایر موارد
            else:
                widget.attrs["class"] = "form-control"


class BootstrapReadOnlyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            widget.attrs["readonly"] = True

            # Input های معمولی
            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.URLInput,
                    forms.TelInput,
                )
            ):
                widget.attrs["class"] = "form-control"

            # Textarea
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("rows", 3)

            # Select
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"

            # Checkbox
            elif isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = "form-check-input"

            # File
            elif isinstance(widget, forms.FileInput):
                widget.attrs["class"] = "form-control"

            # Date / DateTime
            elif isinstance(widget, (forms.DateInput, forms.DateTimeInput)):
                widget.attrs["class"] = "form-control"
                widget.attrs.setdefault("type", "date")

            # سایر موارد
            else:
                widget.attrs["class"] = "form-control"