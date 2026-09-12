from logging import Logger

from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone as tz
from django.core.mail import send_mail

from main.models.enrollment import Enrollment
from main.types import EnrollmentStatus
from main.models import SurveyQuestion, SurveyAnswer, SurveyAnschoice

logger = Logger(__name__)


class SurveyView(LoginRequiredMixin, View):
    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get_context_date(self):
        questions = SurveyQuestion.objects.all()
        anschoices = SurveyAnschoice.objects.all()
        return {
            "questions": questions,
            "anschoices": anschoices,
        }

    def get(self, request):
        context = self.get_context_date()
        return render(request, "pages/survey.html", context)

    def post(self, request):
        data = request.POST.copy()
        current_enrollment = Enrollment.objects.select_related("offer__contract").filter(
            guardian=request.user,
            status=EnrollmentStatus.PENDING
        ).order_by("id").last()
        # check for enrollment existance
        if not current_enrollment:
            messages.error(request, "فعلا ثبت نامی برای انجام نظرسنجی ندارید.")
            return redirect("/dashboard")
        now = tz.now()
        if current_enrollment.offer.contract.poll_start_date > now:
            messages.error(request, "مهلت نظرسنجی هنوز آغاز نشده.")
            return redirect("/dashboard")
        if current_enrollment.offer.contract.poll_end_date < now:
            messages.error(request, "مهلت نظرسنجی به اتمام رسیده است.")
            return redirect("/dashboard")
        answers = []
        del data["csrfmiddlewaretoken"]
        for question_id, choice_id in data.items():
            answers.append(
                SurveyAnswer(enrollment=current_enrollment, question_id=question_id, anschoice_id=choice_id)
            )
        try:
            SurveyAnswer.objects.bulk_create(answers)
        except Exception as e:
            logger.error(str(e), *e.args)
            messages.error(request, "خطایی رخ داد. لطفا با پشتیبانی تماس حاصل فرمایید.")
            return redirect("/dashboard")
        return redirect("/survey")
