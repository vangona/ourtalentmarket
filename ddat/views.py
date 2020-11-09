from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Market, Wants
from tmuser.models import Tmuser
from .forms import MarketForm
from mypage.models import Note

# Create your views here.
def logout(request):
    if request.session.get("user"):
        del request.session["user"]

    return redirect("/")


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
            notes = Note.objects.filter(receiver=userinfo).order_by("-id")
            counts = notes.count()

            context["counts"] = counts
            context["userinfo"] = userinfo

            return context

    # def post(self, request):
    #     if (request.POST.get("market_name") != None) and (
    #         request.POST.get("summary") == None
    #     ):
    #         if not (
    #             request.POST.get("market_name", None)
    #             and request.POST.get("index_name", None)
    #             and request.POST.get("content", None)
    #             and request.FILES.values()
    #         ):
    #             messages.error(request, f"모든 항을 입력하셔야합니다.")

    #             return redirect("/#")

    #         else:

    #             userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
    #             market_name = request.POST.get("market_name", None)
    #             index_name = request.POST.get("index_name", None)
    #             content = request.POST.get("content", None)
    #             for file in request.FILES.values():
    #                 Market.objects.create(
    #                     admin=userinfo,
    #                     market_name=market_name,
    #                     index_name=index_name,
    #                     image=file,
    #                     content=content,
    #                 )

    #                 subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
    #                 message = f"{content} \n http://vangona.pythonanywhere.com/admin"
    #                 mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
    #                 mail.send()

    #                 messages.success(
    #                     request, f"{market_name}, 성공적으로 제출 되었습니다.\n학생증 인증 후 사용 가능합니다."
    #                 )

    #                 return redirect("/#")

    #     elif (request.POST.get("market_name") == None) and (
    #         request.POST.get("summary") != None
    #     ):
    #         userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
    #         username = userinfo.username
    #         usernickname = userinfo.usernickname
    #         useremail = userinfo.useremail
    #         phonenumber = userinfo.phonenumber
    #         department_name = userinfo.department_name
    #         student_number = userinfo.student_number
    #         summary = (request.POST.get("summary", None),)
    #         index_name_w = (request.POST.get("index_name_w", None),)
    #         content_w = request.POST.get("content_w", None)

    #         wants = Wants.objects.create(
    #             username=username,
    #             usernickname=usernickname,
    #             useremail=useremail,
    #             phonenumber=phonenumber,
    #             department_name=department_name,
    #             student_number=student_number,
    #             summary=request.POST.get("summary", None),
    #             index_name_w=request.POST.get("index_name_w", None),
    #             content_w=request.POST.get("content_w", None),
    #         )

    #         subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
    #         message = f"{content_w} \n http://vangona.pythonanywhere.com/admin"
    #         mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
    #         mail.send()

    #         messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

    #         return redirect("/#")


# def Index(request):
#     if request.method == "GET":
#         if request.session.get("user") != None:
#             userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
#             return render(request, "index.html", {"userinfo": userinfo})
#         else:
#             return render(request, "index.html")
#     elif (request.method == "POST") and (request.POST.get("market_name") != None):
#         userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
#         market_name = request.POST.get("market_name", None)
#         index_name = request.POST.get("index_name", None)
#         content = request.POST.get("content", None)

#         res_data = {}

#         if not (market_name and index_name and content):
#             res_data["error"] = f"{market_name, index_name, content}"
#         else:
#             market = Market(
#                 username=userinfo.username,
#                 usernickname=userinfo.usernickname,
#                 useremail=userinfo.useremail,
#                 phonenumber=userinfo.phonenumber,
#                 department_name=userinfo.department_name,
#                 student_number=userinfo.student_number,
#                 market_name=market_name,
#                 index_name=index_name,
#                 content=content,
#             )

#             market.save()

#             subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
#             message = f"{content} \n http://vangona.pythonanywhere.com/admin"
#             mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
#             mail.send()

#             return render(
#                 request,
#                 "result.html",
#                 {
#                     "res_data": res_data,
#                     "market": market,
#                     "index": 0,
#                     "userinfo": userinfo,
#                 },
#             )

#     elif (request.method == "POST") and (request.POST.get("market_name") == None):
#         userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
#         summary = request.POST.get("summary", None)
#         index_name_w = request.POST.get("index_name_w", None)
#         content_w = request.POST.get("content_w", None)

#         res_data = {}

#         if not (summary and index_name_w and content_w):
#             res_data["error"] = "빠진 항목이 있습니다."
#         else:
#             wants = Wants(
#                 username=userinfo.username,
#                 usernickname=userinfo.usernickname,
#                 useremail=userinfo.useremail,
#                 phonenumber=userinfo.phonenumber,
#                 department_name=userinfo.department_name,
#                 student_number=userinfo.student_number,
#                 summary=summary,
#                 index_name_w=index_name_w,
#                 content_w=content_w,
#             )

#             wants.save()

#             subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
#             message = f"{content_w} \n http://vangona.pythonanywhere.com/admin"
#             mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
#             mail.send()

#             return render(
#                 request,
#                 "result.html",
#                 {
#                     "res_data": res_data,
#                     "wants": wants,
#                     "index": 1,
#                     "userinfo": userinfo,
#                 },
#             )


## CBV 참여하기, 2개의 Form이 필요하여 FBV로 작성하게됨. 흔적만 남겨둠 ##

# class MarketView(FormView):
#     template_name = "index.html"
#     form_class = MarketForm
#     success_url = "/"

#     def form_valid(self, form):
#         userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
#         market = Market(
#             username=userinfo.username,
#             usernickname=userinfo.usernickname,
#             useremail=userinfo.useremail,
#             phonenumber=userinfo.phonenumber,
#             department_name=userinfo.department_name,
#             student_number=userinfo.student_number,
#             market_name=form.data.get("market_name"),
#             index_name=form.data.get("index_name"),
#             content=form.data.get("content"),
#         )
#         market.save()

#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         if self.request.session.get("user") != None:
#             context["userinfo"] = Tmuser.objects.get(
#                 useremail=self.request.session.get("user")
#             )
#             return context

#         else:
#             return context
