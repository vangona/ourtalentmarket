from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.db import transaction
from ddat.decorator import login_required, admin_required
from ddat.models import Market, Wants
from tmuser.models import Tmuser
from market.models import TalentMarket
from .models import Content, Questions, Image, Answer
from .forms import WritingForm, QuestionForm, AnswerForm
from django.core.mail import EmailMessage

# Create your views here.
class BoardDetailView(DetailView):
    template_name = "board_detail.html"
    queryset = Image.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["content"] = Image.objects.filter(content_id=self.kwargs["pk"])
        return context


class BoardView(TemplateView):

    template_name = "board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.all()

        return context


@method_decorator(login_required, name="dispatch")
class WriteView(FormView):
    template_name = "write.html"
    form_class = WritingForm
    success_url = "/write/"

    def form_valid(self, form):
     userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
     market = Market.objects.get(id=pk)
     title = form.data.get("title"),
     content = Content.objects.create(
         title=form.data.get("title"),
         description=form.data.get("description"),
         writer=userinfo.usernickname,
     )

     Image.objects.create(content=content, market=market, order=idx)

     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        market = Market.objects.get(id=self.kwargs["pk"])
        context["market"] = market

        return context


class QnaView(TemplateView):
    template_name = "q&a.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            return context

        else:
            return context


class QuestionView(FormView):
    template_name = "ask_answer.html"
    form_class = QuestionForm
    success_url = "/ask/answer/"

    def form_valid(self, form):
        if self.request.session.get("user") != None:
            userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
            title=form.data.get("title")
            content=form.data.get("content")
            questions = Questions(
                username=userinfo.username,
                usernickname=userinfo.usernickname,
                useremail=userinfo.useremail,
                phonenumber=userinfo.phonenumber,
                department_name=userinfo.department_name,
                student_number=userinfo.student_number,
                title=title,
                content=content,
                answered="N",
            )
            questions.save()

            subject = f"새 질문이 들어왔습니다. {userinfo.username}, {title}"
            message = f"{content} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
            mail.send()

            messages.success(self.request, '질문이 등록되었습니다.')

            return super().form_valid(form)

        else:
            title=form.data.get("title")
            content=form.data.get("content")
            questions = Questions(
                username="가입되지 않은 사용자",
                usernickname="익명",
                useremail="anonymous@anonymous.com",
                phonenumber="010-0000-0000",
                department_name="아무개 학과",
                student_number="00000000",
                title=title,
                content=content,
                answered="N",
            )
            questions.save()

            subject = f"새 질문이 들어왔습니다. 가입되지 않은 사용자, {title}"
            message = f"{content} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
            mail.send()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["questions"] = Questions.objects.all()
            return context

        else:
            context["questions"] = Questions.objects.all()
            return context


class QuestionDetailView(TemplateView):
    template_name = "ask_answer_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Questions.objects.filter(id=self.kwargs["pk"])
        answers = Answer.objects.filter(question=Questions.objects.get(id=self.kwargs["pk"]))

        context["questions"] = questions
        context["answers"] = answers

        return context

@method_decorator(admin_required, name="dispatch")
class AnswerView(FormView):
    template_name = "answer_detail.html"
    form_class = AnswerForm
    success_url = "/ask/answer/answer/"

    def form_valid(self, form, **kwargs):
        with transaction.atomic():
            userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
            question=Questions.objects.get(id=form.data.get("question"))
            answer = Answer(
                question=question,
                title=form.data.get("title"),
                content=form.data.get("content"),
            )
            answer.save()

            question.answered = "Y"
            question.save()

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["userinfo"] = Tmuser.objects.get(
            useremail=self.request.session.get("user")
        )
        context["questions"] = Questions.objects.all()
        context["answers"] = Answer.objects.all()
        return context
