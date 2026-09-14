import os
import pandas as pd

from django.views import View
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from common.utils.excel import ExcelToolKit
from common.utils.exceptions import ExcelParserError


class MergeExcelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    excel_toolkit = ExcelToolKit()

    def get(self, request):
        context = admin.site.each_context(request)
        return render(request, "admin/merge_excel.html", context)

    def post(self, request):
        first_file = request.FILES.get("first_file")
        second_file = request.FILES.get("second_file")
        msg1 = self.excel_toolkit.validate_excel_file(first_file)
        msg2 = self.excel_toolkit.validate_excel_file(second_file)
        if msg1:
            messages.error(request, f"فایل اول: {msg1}")
        if msg2:
            messages.error(request, f"فایل دوم: {msg2}")
        if not (msg1 and msg2):
            return self.excel_toolkit.merge_two_excels(first_file, second_file)
        return redirect("/admin/merge-excel")
