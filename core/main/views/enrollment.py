from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def preprocessing(self):
        person_id = self.request.user.person_id
        current_contract_id = CurrentInsuranceContract.current().contract_id
        if Enrollment.objects.filter(
            guardian_id=person_id, offer__contract=current_contract_id
        ).exists():
            return False, "شما از پیش ثبت نام کرده اید."
        return True, ""

    def get(self, request):
        can_resume, msg = self.preprocessing()
        if not can_resume:
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
        form = EnrollmentCreateForm(request.POST)
        if form.is_valid():
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
