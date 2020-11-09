from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from ddat.models import Market, Wants
from .models import Tmuser
from .forms import RegisterForm, LoginForm

# Create your views here.
class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        tmuser = Tmuser(
            useremail=form.data.get("useremail"),
            password=make_password(form.data.get("password")),
            username=form.data.get("username"),
            usernickname=form.data.get("usernickname"),
            phonenumber=form.data.get("phonenumber"),
            department_name=form.data.get("department_name"),
            student_number=form.data.get("student_number"),
            private=form.data.get("private"),
        )
        tmuser.save()

        subject = f"새 회원이 가입했습니다. {tmuser.username}, {tmuser.usernickname}"
        message = f"{tmuser.department_name} \n http://vangona.pythonanywhere.com/admin"
        mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
        mail.send()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        self.request.session["user"] = form.data.get("useremail")

        return super().form_valid(form)


def logout(request):
    if request.session.get("user"):
        del request.session["user"]

    return redirect("/")
