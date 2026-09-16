from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout


class LogoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login")

        is_oidc_user = "oidc_id_token" in request.session

        logout(request)

        if is_oidc_user:
            # اگر با OIDC آمده بود، او را به ان‌پوینت خروج IdP هدایت کن
            idp_logout_url = "https://your-idp-domain.com/oauth/logout/"
            client_post_logout_url = "https://your-client-domain.com/"
            
            # معمولا id_token_hint هم برای امنیت بیشتر ارسال می‌شود
            id_token = request.session.get('oidc_id_token')
            
            redirect_url = f"{idp_logout_url}?post_logout_redirect_uri={client_post_logout_url}"
            if id_token:
                redirect_url += f"&id_token_hint={id_token}"
                
            return redirect(redirect_url)
        else:
            # اگر کاربر عادی بود، فقط به صفحه اصلی یا لاگین خودش هدایت شود
            return redirect('/')
