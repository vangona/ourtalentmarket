from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib import messages
from ddat.decorator import login_required, admin_required
from board.models import Content, Image
from tmuser.models import Tmuser
from ddat.models import Market, Wants
from mypage.models import Note


class BaseView(View):
    @staticmethod
    def response(data={}, message="", status=200):
        result = {
            "data": data,
            "message": message,
        }
        return JsonResponse(result, status=status)


class NoteCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        market = Market.objects.get(id=request.POST.get("receiver")).market_name
        writer = Tmuser.objects.get(useremail=self.request.session.get("user"))
        receiver = Market.objects.get(id=request.POST.get("receiver")).admin

        note = Note.objects.create(
            title=title,
            content=content,
            market=market,
            writer=writer,
            receiver=receiver,
        )

        return self.response({})


class ReplyCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        market_name = request.POST.get("market_name", "")
        writer = Tmuser.objects.get(useremail=self.request.session.get("user"))
        receiver = Tmuser.objects.get(id=request.POST.get("receiver"))

        note = Note.objects.create(
            title=title,
            content=content,
            market=market_name,
            writer=writer,
            receiver=receiver,
        )

        return self.response({})


@method_decorator(login_required, name="dispatch")
class ContentCreateView(BaseView):
    def post(self, request, pk):
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        writer = Tmuser.objects.get(
            useremail=self.request.session.get("user")
        ).usernickname

        market = Market.objects.get(id=pk)

        content = Content.objects.create(
            title=title, description=description, writer=writer
        )

        images = request.FILES.values()


        for idx, file in enumerate(images):
            Image.objects.create(content=content, image=file, market=market, order=idx)

        if not request.FILES :
            idx = 0
            Image.objects.create(content=content, market=market, order=idx)

        messages.success(request, "성공적으로 등록 되었습니다.")

        return self.response({})


@method_decorator(login_required, name="dispatch")
class MarketCreateView(BaseView):
    def post(self, request):
        admin = Tmuser.objects.get(useremail=self.request.session.get("user"))
        market_name = request.POST.get("market_name", "")
        index_name = request.POST.get("index_name", "")
        content = request.POST.get("content", "")
        authorization = "N"

        for file in enumerate(request.FILES.values()):
            Market.objects.create(
                admin=admin,
                market_name=market_name,
                index_name=index_name,
                content=content,
                authorization=authorization,
                image=file,
            )

        subject = f"새 장돌뱅이가 들어왔습니다. {admin.username}, {market_name}"
        message = f"{content} \n https://www.ourtalentmarket.com/admin"
        mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
        mail.send()

        return self.response({})


@method_decorator(login_required, name="dispatch")
class WantCreateView(BaseView):
    def post(self, request):

        if (request.POST.get("market_name") == None) and (
            request.POST.get("summary") != None
        ):
            admin = Tmuser.objects.get(useremail=self.request.session.get("user"))
            summary = request.POST.get("summary", "")
            index_name_w = request.POST.get("index_name_w", "")
            content_w = request.POST.get("content_w", "")

            for idx, file in enumerate(request.FILES.values()):
                Market.objects.create(
                    admin=admin,
                    summary=summary,
                    index_name_w=index_name_w,
                    content_w=content_w,
                )

            subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
            message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
            mail.send()

            messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

            return self.response({})