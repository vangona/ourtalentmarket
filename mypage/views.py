from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from ddat.decorator import login_required, admin_required
from .models import Note
from ddat.models import Market
from market.models import TalentMarket, Group, Handcraft
from tmuser.models import Tmuser
from .forms import MypageUpdateForm

# Create your views here.


class NoteView(TemplateView):

    template_name = "note.html"


@method_decorator(login_required, name="dispatch")
class MypageView(TemplateView):

    template_name = "mypage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
        if Market.objects.filter(admin=userinfo) != None:
            markets = Market.objects.filter(admin=userinfo)
            for market in markets:
                market_a = []
                if market.authorization == "N":
                    market_a.append(market)

                context["market_a"] = market_a

        if TalentMarket.objects.filter(admin=userinfo) != None:
            talentmarkets = TalentMarket.objects.filter(admin=userinfo)
            context["talentmarkets"] = talentmarkets

        if Group.objects.filter(admin=userinfo) != None:
            groups = Group.objects.filter(admin=userinfo)
            context["groups"] = groups

        if Handcraft.objects.filter(admin=userinfo) != None:
            handcrafts = Handcraft.objects.filter(admin=userinfo)
            context["handcrafts"] = handcrafts

        if Note.objects.filter(receiver=userinfo).order_by("-id"):
            notes = Note.objects.filter(receiver=userinfo).order_by("-id")
            counts = notes.count()
            context["notes"] = notes
            context["counts"] = counts

        context["userinfo"] = userinfo

        return context


@method_decorator(login_required, name="dispatch")
class ReadNoteView(TemplateView):

    template_name = "read_note.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
        markets = Market.objects.filter(admin=userinfo)

        notes = Note.objects.filter(receiver=userinfo).order_by("-id")

        context["userinfo"] = userinfo
        context["markets"] = markets
        context["notes"] = notes

        return context


@method_decorator(login_required, name="dispatch")
class ReadNoteDetailView(DetailView):
    template_name = "read_note_detail.html"
    queryset = Note.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userinfo = Tmuser.objects.get(id=self.kwargs["user"])
        notes = Note.objects.get(id=self.kwargs["pk"])
        all_boards = Note.objects.filter(receiver=userinfo).order_by("-id")
        page = int(self.request.GET.get("p", 1))
        paginator = Paginator(all_boards, 1)

        context["boards"] = paginator.get_page(page)
        context["userinfo"] = userinfo
        context["notes"] = notes
        return context


def NoteDeleteView(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()

    return redirect("/mypage/note/read")


@method_decorator(login_required, name="dispatch")
class MypageUpdateView(FormView):
    template_name = "mypage_update.html"
    form_class = MypageUpdateForm
    success_url = "/mypage/"

    def form_valid(self, form):
        userinfo = Tmuser.objects.get(useremail=self.request.session.get("user"))
        usernickname = form.data.get("usernickname")
        phonenumber = form.data.get("phonenumber")

        if usernickname != None:
            userinfo.usernickname = usernickname

        if phonenumber != None:
            userinfo.phonenumber = phonenumber

        userinfo.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userinfo"] = Tmuser.objects.get(
            useremail=self.request.session.get("user")
        )

        return context
