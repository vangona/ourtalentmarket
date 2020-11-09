from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404
from ddat.decorator import login_required, admin_required
from ddat.models import Market, Wants
from ddat.forms import MarketForm, WantsForm
from tmuser.models import Tmuser
from market.models import TalentMarket, Handcraft, Group
from notice.models import MainModel
from board.models import Image
from .forms import MarketUpdateForm

# 재능장


class MarketView(TemplateView):

    template_name = "market.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="재능장").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["boards"] = TalentMarket.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="재능장").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["boards"] = TalentMarket.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

    def post(self, request):
        with transaction.atomic():
            if request.POST.get("market_name") != None:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                market_name = request.POST.get("market_name", "")
                index_name = request.POST.get("index_name", "")
                image = self.request.FILES.get("image")
                content = request.POST.get("content", "")

                if not (market_name and index_name and image and content):
                    messages.error(request, "제출에 실패했습니다. 모든 항목을 채워야합니다.")

                    return redirect("/board/market/")

                else:
                    market = Market.objects.create(
                        admin=admin,
                        market_name=market_name,
                        index_name=index_name,
                        image=image,
                        content=content,
                        authorization="N",
                    )

                    subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
                    message = f"{content} \n https://www.ourtalentmarket.com/admin"
                    mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                    mail.send()

                    messages.success(request, f"{market_name}, 성공적으로 제출 되었습니다.")

                    return redirect("/board/market/")

            else:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                summary = request.POST.get("summary", None)
                index_name_w = request.POST.get("index_name_w", None)
                content_w = request.POST.get("content_w", None)

                wants = Wants.objects.create(
                    admin=admin,
                    summary=request.POST.get("summary", None),
                    index_name_w=request.POST.get("index_name_w", None),
                    content_w=request.POST.get("content_w", None),
                )

                subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
                message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
                mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                mail.send()

                messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

                return redirect("/board/market/")


@method_decorator(login_required, name="dispatch")
class MarketRegisterView(FormView):
    template_name = "market_register.html"
    form_class = MarketForm
    success_url = "/board/market/"

    def form_valid(self, form):
        with transaction.atomic():
            userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
            market_name = form.data.get("market_name")
            index_name = form.data.get("index_name")
            content = form.data.get("content")

            market = Market(
                admin=userinfo,
                market_name=market_name,
                index_name=index_name,
                image=self.request.FILES.get("image"),
                content=content,
                authorization="N",
            )
            market.save()

            subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
            message = f"{content} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
            mail.send()

            messages.success(
                self.request, f"{market_name}, 성공적으로 제출 되었습니다.\n학생증 인증 후 사용 가능합니다."
            )

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            return context

        else:
            return context


@method_decorator(login_required, name="dispatch")
class WantRegisterView(FormView):
    template_name = "want_register.html"
    form_class = WantsForm
    success_url = "/board/market/"

    def form_valid(self, form):
        with transaction.atomic():
            userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
            wants = Wants(
                admin=userinfo,
                summary=form.data.get("summary"),
                index_name_w=form.data.get("index_name_w"),
                content_w=form.data.get("content_w"),
            )
            wants.save()

            subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
            message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
            mail.send()

            messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            return context

        else:
            return context


@method_decorator(login_required, name="dispatch")
class MarketUpdateView(FormView):
    template_name = "market_update.html"
    form_class = MarketUpdateForm
    success_url = "/mypage/"

    def form_valid(self, form):
        userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
        market = Market.objects.get(
            market_name=self.request.POST.get("market_for_update")
        )
        market_name = form.data.get("market_name")
        content = form.data.get("content")
        image = self.request.FILES.get("image")

        if market_name != "":
            market.market_name = market_name

        if content != "":
            market.content = content

        if image != None:
            market.image = image

        market.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
        markets = Market.objects.filter(admin=userinfo)

        context["userinfo"] = userinfo
        context["markets"] = markets

        return context


def BoardDeleteView(request, pk):
    board = Image.objects.get(id=pk)
    board.delete()

    return redirect("/mypage/note/read")


class MarketDetailView(DetailView):
    template_name = "market_detail.html"
    queryset = TalentMarket.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        market = TalentMarket.objects.get(id=self.kwargs["pk"])
        context["market"] = market
        context["boards"] = Image.objects.filter(market=market).order_by('-id')

        return context


class MarketBoardDetailView(DetailView):
    template_name = "market_board_detail.html"
    queryset = Image.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        market = Market.objects.get(id=self.kwargs["market"])
        all_boards = Image.objects.filter(market=market).order_by("-id")
        page = int(self.request.GET.get("p", 1))
        paginator = Paginator(all_boards, 1)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )

        context["boards"] = paginator.get_page(page)

        return context


# 소공예품


class HandcraftView(TemplateView):

    template_name = "handcraft.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="수공예품").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["boards"] = Handcraft.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="수공예품").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["boards"] = Handcraft.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

    def post(self, request):
        with transaction.atomic():
            if request.POST.get("market_name") != None:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                market_name = request.POST.get("market_name", "")
                index_name = request.POST.get("index_name", "")
                image = self.request.FILES.get("image")
                content = request.POST.get("content", "")

                if not (market_name and index_name and image and content):
                    messages.error(request, "제출에 실패했습니다. 모든 항목을 채워야합니다.")

                    return redirect("/board/handcraft/")

                else:
                    market = Market.objects.create(
                        admin=admin,
                        market_name=market_name,
                        index_name=index_name,
                        image=image,
                        content=content,
                        authorization="N",
                    )

                    subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
                    message = f"{content} \n https://www.ourtalentmarket.com/admin"
                    mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                    mail.send()

                    messages.success(request, f"{market_name}, 성공적으로 제출 되었습니다.")

                    return redirect("/board/handcraft/")

            else:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                summary = request.POST.get("summary", None)
                index_name_w = request.POST.get("index_name_w", None)
                content_w = request.POST.get("content_w", None)

                wants = Wants.objects.create(
                    admin=admin,
                    summary=request.POST.get("summary", None),
                    index_name_w=request.POST.get("index_name_w", None),
                    content_w=request.POST.get("content_w", None),
                )

                subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
                message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
                mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                mail.send()

                messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

                return redirect("/board/handcraft/")


class HandcraftDetailView(DetailView):
    template_name = "handcraft_detail.html"
    queryset = Handcraft.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        market = Handcraft.objects.get(id=self.kwargs["pk"])

        context["market"] = market
        context["boards"] = Image.objects.filter(market=market).order_by('-id')
        return context


# 소모임


class GroupView(TemplateView):

    template_name = "group.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="소모임").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["boards"] = Group.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            all_boards = Wants.objects.filter(index_name_w="소모임").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["boards"] = Group.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

    def post(self, request):
        with transaction.atomic():
            if request.POST.get("market_name") != None:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                market_name = request.POST.get("market_name", "")
                index_name = request.POST.get("index_name", "")
                image = self.request.FILES.get("image")
                content = request.POST.get("content", "")

                if not (market_name and index_name and image and content):
                    messages.error(request, "제출에 실패했습니다. 모든 항목을 채워야합니다.")

                    return redirect("/board/group/")

                else:
                    market = Market.objects.create(
                        admin=admin,
                        market_name=market_name,
                        index_name=index_name,
                        image=image,
                        content=content,
                        authorization="N",
                    )

                subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
                message = f"{content} \n https://www.ourtalentmarket.com/admin"
                mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                mail.send()

                messages.success(request, f"{market_name}, 성공적으로 제출 되었습니다.")

                return redirect("/board/group/")

            else:
                userinfo = Tmuser.objects.get(useremail=request.session.get("user"))
                admin = userinfo
                summary = request.POST.get("summary", None)
                index_name_w = request.POST.get("index_name_w", None)
                content_w = request.POST.get("content_w", None)

                wants = Wants.objects.create(
                    admin=userinfo,
                    summary=request.POST.get("summary", None),
                    index_name_w=request.POST.get("index_name_w", None),
                    content_w=request.POST.get("content_w", None),
                )

                subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
                message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
                mail = EmailMessage(subject, message, to=["rlarhksrud14@gmail.com"])
                mail.send()

                messages.success(request, f"{summary}, 성공적으로 제출 되었습니다.")

                return redirect("/board/group/")


class GroupDetailView(DetailView):
    template_name = "group_detail.html"
    queryset = Group.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        market = Group.objects.get(id=self.kwargs["pk"])

        context["market"] = market
        context["boards"] = Image.objects.filter(market=market).order_by('-id')
        return context