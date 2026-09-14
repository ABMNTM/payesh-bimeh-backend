from django.views import View
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from common.utils.excel import (
    all_person_fields,
    all_person_fieldnames,
    all_user_fields,
    all_user_fieldnames,
    ExcelToolKit
)
from main.models.insurance_contract import InsuranceContract


class ReportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    excel_toolkit = ExcelToolKit()

    def get(self, request):
        context = admin.site.each_context(request)
        context["contracts"] = InsuranceContract.objects.all()
        context["all_person_fields"] = [
            {
                "key": all_person_fields[i],
                "value": all_person_fieldnames[i]
            } for i in range(len(all_person_fieldnames))
        ]
        context["all_user_fields"] = [
            {
                "key": all_user_fields[i],
                "value": all_user_fieldnames[i],
            } for i in range(len(all_user_fieldnames))
        ]
        return render(request, "admin/report.html", context)

    def post(self, request):
        user_fields = request.POST.getlist("user_field")
        person_fields = request.POST.getlist("person_field")
        contract_id = request.POST.get("contract")
        try:
            contarct = InsuranceContract.objects.get(pk=contract_id)
            return self.excel_toolkit.export_to_excel(contarct, user_fields, person_fields)
        except AssertionError as e:
            messages.error(request, e.args[0])
        except InsuranceContract.DoesNotExist:
            messages.error(request, "قرارداد موردنظر یافت نشد.")
        return redirect("/admin/report")
