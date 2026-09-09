"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from accounts.views.login import LoginView
from accounts.views.logout import LogoutView
from accounts.views.profile import ProfileView
from main.views.enrollment import EnrollmentView, SeePriceView
from main.views.persons import PersonsView, CreatePersonView, UpdatePersonsView
from main.views.dashboard import DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path("persons/", PersonsView.as_view(), name="persons"),
    path("persons/create", CreatePersonView.as_view(), name="create_person"),
    path("persons/<int:pk>/update", UpdatePersonsView.as_view(), name="update_person"),

    path("enroll/", EnrollmentView.as_view(), name="enroll"),
    path("enroll/<int:pk>/see-price/", SeePriceView.as_view(), name="see_price"),

    path("profile/", ProfileView.as_view(), name="profile")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
