from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from accounts.views.login import LoginView
from accounts.views.oidc_login import OIDCLoginView
from accounts.views.logout import LogoutView
from accounts.views.profile import ProfileView
from main.views.survey import SurveyView
from main.views.enrollment import EnrollmentView, SeePriceView
from main.views.persons import PersonsView,CreateHouseholdView, CreatePersonView, UpdatePersonsView
from main.views.dashboard import DashboardView
from main.views.report import ReportView
from main.views.import_excel import ImportExcelView
from main.views.merge_excel import MergeExcelView

urlpatterns = [
    path("admin/report/", ReportView.as_view(), name="report"),
    path("admin/import-excel/", ImportExcelView.as_view(), name="import_excel"),
    path("admin/merge-excel/", MergeExcelView.as_view(), name="merge_excel"),
    path("admin/", admin.site.urls),
    path('captcha/', include('captcha.urls')),

    path("login/", LoginView.as_view(), name="login"),
    path("login/oidc/", OIDCLoginView.as_view(), name="oidc_login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path("persons/", PersonsView.as_view(), name="persons"),
    path("persons/household/create/", CreateHouseholdView.as_view(), name="create_household_person"),
    path("persons/create", CreatePersonView.as_view(), name="create_person"),
    path("persons/<int:pk>/update", UpdatePersonsView.as_view(), name="update_person"),

    path("enroll/", EnrollmentView.as_view(), name="enroll"),
    path("enroll/<int:pk>/see-price/", SeePriceView.as_view(), name="see_price"),

    path("profile/", ProfileView.as_view(), name="profile"),

    path("survey/", SurveyView.as_view(), name="survey"),
    path('oidc/', include('mozilla_django_oidc.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
