import os
import pandas as pd

from django.views import View
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from common.utils.excel import ExcelToolKit
from common.utils.exceptions import ExcelParserError


class ImportExcelView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    excel_toolkit = ExcelToolKit()

    def get(self, request):
        context = admin.site.each_context(request)
        return render(request, "admin/import_excel.html", context)

    def post(self, request):
        excel_file = request.FILES.get("excel_file")
        msg = self.excel_toolkit.validate_excel_file(excel_file)
        if not msg:
            try:
                self.excel_toolkit.import_from_excel(excel_file)
                messages.success(request, "اطلاعات فایل با موفقیت اضافه شد.")
            except ExcelParserError as e:
                messages.error(request, e.args[0])
        else:
            messages.error(request, msg)
        return redirect("/admin/import-excel")
