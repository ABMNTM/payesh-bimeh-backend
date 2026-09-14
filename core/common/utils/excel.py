import pandas as pd
import os
import numpy as np

from io import BytesIO

from django.http import HttpResponse
from django.db import transaction

from openpyxl.styles import Font, Alignment, PatternFill
from accounts.models.user import User
from main.models import Enrollment, Person, EmploymentType

from common.utils.exceptions import ExcelParserError


all_user_fields = (
    "employment_type",
    "personnel_code",
    "organization_enter_year",
    "birth_year",
    "birth_month",
    "birth_day",
    "birth_place",
    "bc_issuance_place",
    "gender",
    "phone_number",
    "landline_number",
    "address",
    "postal_code",
    "organizational_unit",
    "veteran_status",
    "account_number",
    "iba_number",
    "card_number",
    "description",
    "extra_text_5",
    "extra_text_6",
    "extra_text_7",
    "extra_text_8",
    "extra_text_9",
    "post_title",
    "education_certificate",
    "available_services",
    "insured_computer_code",
)

all_user_fieldnames = (
    "نوع استخدام",
    "شماره پرسنلی",
    "سال ورود به سازمان",
    "سال تولد",
    "ماه تولد",
    "روز تولد",
    "محل تولد",
    "محل صدور شناسنامه",
    "جنسیت",
    "شماره موبایل",
    "شماره تلفن ثابت",
    "نشانی",
    "کد پستی",
    "واحد سازمانی",
    "وضعیت ایثارگری",
    "شماره حساب",
    "شماره شبا",
    "شماره کارت",
    "توضیحات",
    "متن اضافه 5",
    "متن اضافه 6",
    "متن اضافه 7",
    "متن اضافه 8",
    "متن اضافه 9",
    "عنوان پست",
    "مدرک تحصیلی",
    "خدمات قابل ارائه",
    "کد رایانه بیمه شده",
)

all_person_fields = (
    "first_name",
    "last_name",
    "national_code",
    "birth_date",
    "birth_certificate_number",
    "father_name",
    "relation_type",
    "tracking_code",
    "educational_certificate",
    "edu_in_progress",
    "is_married",
)

all_person_fieldnames = (
    "نام",
    "نام خانوادگی",
    "کد ملی",
    "تاریخ تولد",
    "شماره شناسنامه",
    "نام پدر",
    "نسبت با سرپرست",
    "کد رهگیری",
    "آخرین مدرک تحصیلی",
    "در حال تحصیل؟",
    "ازدواج کرده؟",
)


class ExcelToolKit:
    def export_to_excel(self, contract, user_fields: list[str], person_fields: list[str]):
        assert set(user_fields).issubset(set(all_user_fields)), "خطا: فیلد های کاربر باید معتبر باشند."
        assert set(person_fields).issubset(set(all_person_fields)), "خطا: فیلد های شخص باید معتبر باشند."
        report_data = []
        for enrollment in Enrollment.objects.select_related("guardian", "guardian__person").prefetch_related(
            "covered_members"
        ).filter(offer__contract=contract):
            report_data.append({
                "RecordType": "سرپرست",
                **{
                    key: getattr(enrollment.guardian.person, key, None)
                    for key in person_fields
                },
                "space": None,
                **{
                    key: getattr(enrollment.guardian, key, None)
                    for key in user_fields
                }
            })
            for member in enrollment.covered_members.all():
                report_data.append({
                    "RecordType": "تحت تکفل"
                    **{
                        key: getattr(member, key, None)
                        for key in person_fields
                    },
                    "space": None,
                    **{
                        key: None
                        for key in user_fields
                    }
                })

        df = pd.DataFrame(report_data)
        buff = BytesIO()
        sheet_name = 'گزارش جامع قرارداد {}'.format(contract.contract_year)
        with pd.ExcelWriter(buff, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)

            # Access the underlying openpyxl workbook and worksheet
            worksheet = writer.sheets[sheet_name]

            # Define styles for Parents and Children
            parent_font = Font(bold=True, color="000000")
            parent_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid") # Light blue background
            child_alignment = Alignment(indent=3) # Indent children to the right

            # Apply styles row by row (skip row 1 because it's the header)
            for row_idx in range(2, worksheet.max_row + 1):
                record_type = worksheet.cell(row=row_idx, column=1).value
                
                if record_type == 'سرپرست':
                    # Style the entire parent row
                    for col_idx in range(1, worksheet.max_column + 1):
                        cell = worksheet.cell(row=row_idx, column=col_idx)
                        cell.font = parent_font
                        cell.fill = parent_fill

                elif record_type == 'تحت تکفل':
                    # Indent the Name and Details columns (Columns 3 and 4) for children
                    for col_idx in range(3, worksheet.max_column + 1):
                        cell = worksheet.cell(row=row_idx, column=col_idx)
                        cell.alignment = child_alignment
        
        response = HttpResponse(
            buff.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="report.xlsx"'

        return response

    def import_from_excel(self, file_content):
        df = pd.read_excel(file_content)
        df = df.replace({np.nan: ""})
        df = df.astype(str)
        employment_dict = self.get_employment_types()
        current_index = 0
        try:
            with transaction.atomic():
                current_person = None
                for idx, row in df.iterrows():
                    current_index = idx
                    if row["RecordType"] == "سرپرست":
                        is_person_data = True
                        person_data = dict()
                        user_data = dict()
                        for col, data in row.items():
                            if col == "RecordType":
                                continue
                            if col == "space":
                                is_person_data = False
                                continue
                            if col == "employment_type":
                                user_data["employment_type_id"] = employment_dict.get(data)
                                continue

                            if is_person_data:
                                person_data[col] = data
                            else:
                                user_data[col] = data
                        person_data = {
                            key: None if value == "" else value for key, value in person_data.items()
                        }
                        print("user_data =", user_data)
                        current_person = Person.objects.create(**person_data, is_household_head=True)
                        User.objects.create(**user_data, person=current_person)

                    elif row["RecordType"] == "تحت تکفل":
                        person_data = dict()
                        for col, data in row.items():
                            if col == "RecordType":
                                continue
                            if col == "space":
                                break
                            person_data[col] = data
                        Person.objects.create(**person_data, is_household_head=False, household=current_person)
                    else:
                        raise Exception("نوع رکورد نامعتبر")
        except Exception as e:
            raise ExcelParserError(f"{e} در سطر {current_index}")

    def merge_two_excels(self, first_file, second_file, key="national_code"):
        first_df = pd.read_excel(first_file)
        second_df = pd.read_excel(second_file)
        final_df = pd.concat([first_df, second_df], ignore_index=True).drop_duplicates(
            subset=['national_code']
        )

        buff = BytesIO()

        with pd.ExcelWriter(buff, engine="openpyxl") as writer:
            final_df.to_excel(writer, index=False, sheet_name=f"ادغام {first_file.name} و {second_file.name}")

        response = HttpResponse(
            buff.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="concated_report.xlsx"'

        return response

    def validate_excel_file(self, file):
        ext = os.path.splitext(file.name)[1].lower()

        if ext not in [".xlsx", ".xls"]:
            return "فقط فایل‌های Excel با فرمت xlsx یا xls قابل قبول هستند."

        try:
            pd.read_excel(file)
        except Exception:
            return "فایل Excel معتبر نیست یا قابل خواندن نمی‌باشد."

    def get_employment_types(self):
        all_employment_types = EmploymentType.objects.all()
        return {
            emp_type.title: emp_type.pk
            for emp_type in all_employment_types
        }
