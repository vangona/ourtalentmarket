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
from board.models import Image, Comment, Content
from .forms import MarketUpdateForm, MarketBoardUpdateForm

# 재능장


class MarketView(TemplateView):

    template_name = "market.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="재능장").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["markets"] = markets
            context["boards"] = TalentMarket.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="재능장").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["markets"] = markets
            context["boards"] = TalentMarket.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context


@method_decorator(login_required, name="dispatch")
class MarketRegisterView(FormView):
    template_name = "market_register.html"
    form_class = MarketForm
    success_url = "/mypage/"

    def form_valid(self, form):
        with transaction.atomic():
            userinfo = Tmuser.objects.get(
                useremail=self.request.session.get("user"))
            market_name = form.data.get("market_name")
            index_name = form.data.get("index_name")
            content = form.data.get("content")
            campus = form.data.get("campus")

            market = Market(
                admin=userinfo,
                market_name=market_name,
                index_name=index_name,
                image=self.request.FILES.get("image"),
                content=content,
                authorization="N",
                campus=campus,
            )
            market.save()

            subject = f"새 장돌뱅이가 들어왔습니다. {userinfo.username}, {market_name}"
            message = f"{content} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=[
                                "rlarhksrud14@gmail.com"])
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
            userinfo = Tmuser.objects.get(
                useremail=self.request.session.get("user"))
            summary = form.data.get("summary")
            index_name_w = form.data.get("index_name_w")
            content_w = form.data.get("content_w")

            wants = Wants(
                admin=userinfo,
                summary=summary,
                index_name_w=index_name_w,
                content_w=content_w,
            )
            wants.save()

            subject = f"새로운 바램이 들어왔습니다. {summary}, {index_name_w}"
            message = f"{content_w} \n https://www.ourtalentmarket.com/admin"
            mail = EmailMessage(subject, message, to=[
                                "rlarhksrud14@gmail.com"])
            mail.send()

            messages.success(self.request, f"{summary}, 성공적으로 제출 되었습니다.")

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

    def form_valid(self, form):
        userinfo = Tmuser.objects.get(
            useremail=self.request.session.get("user"))
        market = Market.objects.get(
            market_name=form.data.get("market_for_update")
        )

        if market.admin == userinfo:

            market_name = form.data.get("market_name")
            content = form.data.get("content")
            select_name = form.data.get("select_name")
            image = self.request.FILES.get("image")

            if market_name:
                market.market_name = market_name

            if content:
                market.content = content

            if select_name:
                market.select_name = select_name

            if image != None:
                market.image = image

            market.save()

            messages.success(self.request, '수정에 성공하셨습니다.')

            return super().form_valid(form)

        else:

            messages.error(self.request, '권한이 없습니다.')

            return super().form_valid(form)

    def get_success_url(self):

        market = Market.objects.get(id=self.kwargs["pk"])

        if market.index_name == "재능장":
            index_name = "market"
        if market.index_name == "소모임":
            index_name = "group"
        if market.index_name == "수공예품":
            index_name = "handcraft"

        success_url = f"/board/{ index_name }/{ market.id }"

        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = Tmuser.objects.get(
            useremail=self.request.session.get("user"))
        market = Market.objects.get(id=self.kwargs["pk"])

        context["userinfo"] = userinfo
        context["market"] = market

        return context


@method_decorator(login_required, name="dispatch")
class MarketBoardUpdateView(FormView):
    template_name = "market_board_update.html"
    form_class = MarketBoardUpdateForm

    def form_valid(self, form):
        title = form.data.get("title")
        content = form.data.get("content")
        board = Image.objects.get(id=self.kwargs["pk"]).content

        board.title = title
        board.description = content

        board.save()

        messages.success(self.request, '수정에 성공하셨습니다.')

        return super().form_valid(form)

    def get_success_url(self):

        content = Image.objects.get(id=self.kwargs["pk"])
        market = content.market

        if market.index_name == "재능장":
            index_name = "market"
        if market.index_name == "소모임":
            index_name = "group"
        if market.index_name == "수공예품":
            index_name = "handcraft"

        success_url = f"/board/market/detail/{ market.id }/{ content.id }"

        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content = Image.objects.get(id=self.kwargs["pk"])

        context["content"] = content

        return context


def BoardDeleteView(request, pk):
    board = Image.objects.get(id=pk)
    market_id = board.market.id

    if board.market.index_name == "재능장":
        index_name = "market"
    if board.market.index_name == "소모임":
        index_name = "group"
    if board.market.index_name == "수공예품":
        index_name = "handcraft"

    board.delete()

    return redirect(f"/board/{ index_name }/{ market_id }")


def CommentDeleteView(request, pk):
    comment = Comment.objects.get(id=pk)
    board_id = comment.board.id
    market_id = comment.board.market.id

    if comment.board.market.index_name == "재능장":
        index_name = "market"
    if comment.board.market.index_name == "소모임":
        index_name = "group"
    if comment.board.market.index_name == "수공예품":
        index_name = "handcraft"

    if Tmuser.objects.get(useremail=request.session.get("user")) != comment.writer:
        messages.warning(request, '권한 없음')
        return redirect(f"/board/{ index_name }/detail/{ market_id }/{ board_id }")

    else:
        comment.delete()

    return redirect(f"/board/market/detail/{ market_id }/{ board_id }")


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
        content = Image.objects.get(id=self.kwargs["pk"])
        comments = Comment.objects.filter(board=content)

        all_boards = Image.objects.filter(market=market).order_by("-id")
        page = int(self.request.GET.get("p", 1))
        paginator = Paginator(all_boards, 1)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )

        context["boards"] = paginator.get_page(page)
        context["content"] = content
        context["comments"] = comments

        return context


# 소공예품


class HandcraftView(TemplateView):

    template_name = "handcraft.html"

    def get_context_data(self, **kwargs):
        if self.request.session.get("user") != None:
            context = super().get_context_data(**kwargs)
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="수공예품").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["markets"] = markets
            context["boards"] = Handcraft.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="수공예품").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["markets"] = markets
            context["boards"] = Handcraft.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context


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
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="소모임").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            context["markets"] = markets
            context["boards"] = Group.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context

        else:
            context = super().get_context_data(**kwargs)
            markets = Market.objects.all()
            all_boards = Wants.objects.filter(
                index_name_w="소모임").order_by("-id")
            page = int(self.request.GET.get("p", 1))
            paginator = Paginator(all_boards, 10)

            context["markets"] = markets
            context["boards"] = Group.objects.all().order_by("-id")
            context["boards_w"] = paginator.get_page(page)
            context["board_main"] = MainModel.objects.last()

            return context


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
