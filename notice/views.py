from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.http import Http404
from django.db import transaction
from .forms import (
    NoticeregisterForm,
    AuthorizeForm,
    NoticeMainForm,
    MarketMainForm,
    IdAuthorizationForm,
)
from ddat.decorator import login_required, admin_required
from tmuser.models import Tmuser, WaitingId
from ddat.models import Market
from market.models import TalentMarket, Group, Handcraft
from .models import NoticeModel, MainModel

# Create your views here.


@method_decorator(admin_required, name="dispatch")
class AdminView(TemplateView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
            return context

        else:
            return context


class NoticeView(TemplateView):

    template_name = "notice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["notices"] = NoticeModel.objects.all()
        context["notice_main"] = MainModel.objects.last()

        return context


class NoticeDetailView(DetailView):
    template_name = "notice_detail.html"
    queryset = NoticeModel.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["notice"] = NoticeModel.objects.get(id=self.kwargs["pk"])

        return context


@method_decorator(admin_required, name="dispatch")
class NoticeregisterView(FormView):
    template_name = "notice_register.html"
    form_class = NoticeregisterForm
    success_url = "/notice/admin/register/"

    def form_valid(self, form):
        userinfo = Tmuser.objects.get(
            useremail=self.request.session.get("user"))
        notice = NoticeModel(
            title=form.data.get("title"),
            image=self.request.FILES.get("image"),
            content=form.data.get("content"),
            writer=userinfo.usernickname,
        )
        notice.save()

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


@method_decorator(admin_required, name="dispatch")
class NoticeMainView(FormView):
    template_name = "notice_main.html"
    form_class = NoticeMainForm
    success_url = "/notice/admin/noticemain/"

    def form_valid(self, form):
        if form.data.get("main") == "Y":
            notice_main = NoticeModel.objects.get(title=form.data.get("title"))

            main = MainModel.objects.last()

            main.notice = notice_main

            main.save()

            return super().form_valid(form)

        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["notices"] = NoticeModel.objects.all()

        return context


@method_decorator(admin_required, name="dispatch")
class AuthorizeView(FormView):
    template_name = "authorize.html"
    form_class = AuthorizeForm
    success_url = "/notice/admin/authorize/"

    def form_valid(self, form):
        market = Market.objects.get(market_name=form.data.get("market_name"))
        market.authorization = form.data.get("authorization")

        market.save()

        admin = market.admin
        market_name = market.market_name
        index_name = market.index_name
        content = market.content
        image = market.image
        authorization = market.authorization
        registered_dttm = market.registered_dttm
        modified_dttm = market.modified_dttm

        with transaction.atomic():
            if market.index_name == "재능장":
                talentmarket = TalentMarket.objects.create(
                    admin=admin,
                    market_name=market_name,
                    index_name=index_name,
                    content=content,
                    image=image,
                    authorization=authorization,
                    registered_dttm=registered_dttm,
                    modified_dttm=modified_dttm,
                )

                talentmarket.save()
                market.delete()

            elif market.index_name == "수공예품":
                handcraft = Handcraft.objects.create(
                    admin=admin,
                    market_name=market_name,
                    index_name=index_name,
                    content=content,
                    image=image,
                    authorization=authorization,
                    registered_dttm=registered_dttm,
                    modified_dttm=modified_dttm,
                )

                handcraft.save()
                market.delete()

            elif market.index_name == "소모임":
                group = Group.objects.create(
                    admin=admin,
                    market_name=market_name,
                    index_name=index_name,
                    content=content,
                    image=image,
                    authorization=authorization,
                    registered_dttm=registered_dttm,
                    modified_dttm=modified_dttm,
                )

                group.save()
                market.delete()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["markets"] = Market.objects.filter(authorization="N")

        return context


@method_decorator(admin_required, name="dispatch")
class TalentMarketMainView(FormView):
    template_name = "talentmarket_main.html"
    form_class = MarketMainForm
    success_url = "/notice/admin/talentmarketmain/"

    def form_valid(self, form):
        if form.data.get("main") == "Y":
            talentmarket = TalentMarket.objects.get(
                market_name=form.data.get("market_name")
            )

            main = MainModel.objects.last()
            main.talentmarket = talentmarket
            main.talentmarket_main = form.data.get("main_content")

            main.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["markets"] = TalentMarket.objects.all()

        return context


@method_decorator(admin_required, name="dispatch")
class HandcraftMainView(FormView):
    template_name = "handcraft_main.html"
    form_class = MarketMainForm
    success_url = "/notice/admin/handcraftmain/"

    def form_valid(self, form):
        if form.data.get("main") == "Y":
            handcraft = Handcraft.objects.get(
                market_name=form.data.get("market_name"))

            main = MainModel.objects.last()

            main.handcraft = handcraft
            main.handcraft_main = form.data.get("main_content")

            main.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["markets"] = Handcraft.objects.all()

        return context


@method_decorator(admin_required, name="dispatch")
class GroupMainView(FormView):
    template_name = "group_main.html"
    form_class = MarketMainForm
    success_url = "/notice/admin/groupmain/"

    def form_valid(self, form):
        if form.data.get("main") == "Y":
            group = Group.objects.get(market_name=form.data.get("market_name"))

            main = MainModel.objects.last()

            main.group = group
            main.group_main = form.data.get("main_content")

            main.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get("user") != None:
            context["userinfo"] = Tmuser.objects.get(
                useremail=self.request.session.get("user")
            )
        context["markets"] = Group.objects.all()

        return context


@method_decorator(admin_required, name="dispatch")
class IdAuthorizationView(FormView):
    template_name = "id_authorization.html"
    form_class = IdAuthorizationForm
    success_url = "/notice/admin/id_check/"

    def form_valid(self, form):
        waitingid = WaitingId.objects.get(id=form.data.get("user_id"))
        userinfo = Tmuser.objects.get(id=waitingid.waiting_user.id)
        userinfo.id_verification = form.data.get("authorization")

        userinfo.save()

        waitingid.delete()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = WaitingId.objects.all()

        return context
