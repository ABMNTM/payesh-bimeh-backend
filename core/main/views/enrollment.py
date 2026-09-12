from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone as tz
import jdatetime

from main.models.employment_type import EmploymentType
from core.settings import ORGANIZATION_SERVICE_MAX_YEAR
from main.types import EducationalCertificates, RelationshipType
from financial.services.cost_factory import calculate_total_cost

from main.models import Enrollment, CurrentInsuranceContract
from main.forms.enrollment import EnrollmentCreateForm


class EnrollmentView(LoginRequiredMixin, View):
    login_url = "login/"
    redirect_field_name = "redirect_to"

    def get_context_data(self):
        context = dict()
        contract_exists = False
        current_contract = CurrentInsuranceContract.current()
        if current_contract:
            contract_exists = True
            context["current_offers"] = current_contract.contract.offers.all()
            context["dependants"] = self.request.user.person.household_members.all()
        context["contract_exists"] = contract_exists
        return context

    def _get_process_error(self):
        person_id = self.request.user.person_id
        current_contract = CurrentInsuranceContract.current().contract
        now = tz.now()
        if not current_contract:
            return "فعلا دوره بیمه ای برای ثبت نام وجود ندارد."
        if Enrollment.objects.filter(
            guardian_id=person_id, offer_contract=current_contract
        ).exists():
            return "شما از پیش ثبت نام کرده اید."
        if current_contract.signup_start_date > now:
            return "زمان ثبت نام فعلا آغاز نشده است."
        if current_contract.signup_end_date < now:
            return "زمان ثبت نام به پایان رسیده است."

        message = self._check_health_insurance_restriction()
        if message:
            return message

        return

    def _check_for_childs(self, members):
        for member in members:
            if member.relation_type == RelationshipType.S_CHILD:
                max_age = 20
                if not member.edu_in_progress:
                    max_age = 20
                else:
                    match member.educational_certificate:
                        case EducationalCertificates.UNDER_DIPLOMA:
                            max_age = 20
                        case EducationalCertificates.DIPLOMA:
                            max_age = 23
                        case EducationalCertificates.BACHELOR:
                            max_age = 25
                        case EducationalCertificates.GRADUATE:
                            max_age = 27
                        case _:
                            max_age = 20
                if member.age >= max_age:
                    return "کاربر {} {}، به دلیل سن بالاتر از حد مجاز، نمی تواند ثبت نام کند.".format(member.first_name, member.last_name)
            if member.relation_type == RelationshipType.D_CHILD:
                if member.is_married:
                    return "کاربر {} {}، به دلیل تزویج نمی تواند ثبت نام کند.".format(member.first_name, member.last_name)

    def _check_health_insurance_restriction(self):
        user = self.request.user

        if user.organization_enter_year is None:
            return "لطفا برای انجام ثبت نام، سال ورود به سازمان را در صفحه پروفایل تکمیل کنید."

        employment_type = user.employment_type
        if not employment_type:
            return "لطفا برای انجام ثبت نام، نوع کارمندی خود را در صفحه پروفایل وارد کنید."

        if (
            jdatetime.date.today().year - user.organization_enter_year
            >= ORGANIZATION_SERVICE_MAX_YEAR
            and employment_type.title == "کارمند قراردادی"
        ):
            return (
                "همکار گرامی، بیمه شما به دلیل عدم حضور در سامانه بیمه سلامت امکان پذیر نمی باشد.\n\n"
                "جهت ادامه مراحل، با مراجع ذیربط در ارتباط باشید."
            )

        return None

    def get(self, request):
        msg = self._get_process_error()
        if not msg:
            messages.error(request, msg)
            return redirect("/dashboard")
        context = self.get_context_data()
        return render(request, "pages/enrollment.html", context)

    def create_enrollment(self, form):
        members = form.cleaned_data.get("covered_members")
        instance = form.save(commit=False)
        instance.guardian = self.request.user
        instance.total_cost = calculate_total_cost(self.request.user, members)
        instance.save()
        form.save_m2m()

    def post(self, request):
        msg = self._get_process_error()
        if msg:
            messages.error(request, msg)
            return redirect("/dashboard")
        form = EnrollmentCreateForm(request.POST)
        if form.is_valid():
            members = form.cleaned_data.get("covered_members")
            msg = self._check_for_childs(members)
            if msg:
                messages.error(request, msg)
                return redirect("/enroll")
            self.create_enrollment(form)
            messages.success(request, "ثبت نام با موفقیت انجام شد.")
            return redirect("/dashboard")
        for error in form.errors.values():
            messages.error(request, error)
        return redirect("/enroll")


class SeePriceView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request, pk):
        obj = get_object_or_404(Enrollment, pk=pk)
        return render(request, "pages/see_price.html", {"object": obj})
