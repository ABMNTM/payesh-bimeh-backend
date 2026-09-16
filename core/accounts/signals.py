from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver


@receiver(user_login_failed)
def oidc_login_failed(sender, credentials, request, **kwargs):
    from django.contrib import messages
    messages.error(request, "کاربر با کدملی شما یافت نشد. لطفا با پشتیبانی تماس بگیرید.")
