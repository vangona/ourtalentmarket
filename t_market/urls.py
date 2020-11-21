"""t_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from ddat.views import IndexView
from board.views import (
    WriteView,
    QuestionView,
    QnaView,
    BoardView,
    BoardDetailView,
    AnswerView,
    QuestionDetailView,
)
from tmuser.views import RegisterView, LoginView, logout
from notice.views import (
    NoticeView,
    NoticeDetailView,
    NoticeregisterView,
    NoticeMainView,
    AuthorizeView,
    AdminView,
    TalentMarketMainView,
    GroupMainView,
    HandcraftMainView,
)
from market.views import (
    MarketView,
    HandcraftView,
    GroupView,
    MarketDetailView,
    HandcraftDetailView,
    GroupDetailView,
    MarketRegisterView,
    WantRegisterView,
    MarketBoardDetailView,
    MarketUpdateView,
    BoardDeleteView,
    CommentDeleteView,
    MarketBoardUpdateView,
)
from apis.views import (
    ContentCreateView,
    MarketCreateView,
    WantCreateView,
    NoteCreateView,
    ReplyCreateView,
    CommentCreateView,
)
from mypage.views import (
    NoteView,
    MypageView,
    ReadNoteView,
    ReadNoteDetailView,
    NoteDeleteView,
    MypageUpdateView,
)

urlpatterns = [
    path("", IndexView.as_view()),
    path("admin/", admin.site.urls),
    path("board/", NoticeView.as_view()),
    path("board/<int:pk>/", BoardDetailView.as_view()),
    path("board/board/", BoardView.as_view()),
    path("board/market/", MarketView.as_view()),
    path("board/market/delete/<int:pk>", BoardDeleteView),
    path("board/market/board/comment/delete/<int:pk>", CommentDeleteView),
    path("board/market/update/<int:pk>", MarketUpdateView.as_view()),
    path("board/market/board/update/<int:pk>", MarketBoardUpdateView.as_view()),
    path("board/market/<int:pk>", MarketDetailView.as_view()),
    path("board/market/detail/<int:market>/<int:pk>", MarketBoardDetailView.as_view()),
    path("board/market/register/", MarketRegisterView.as_view()),
    path("board/want/register/", WantRegisterView.as_view()),
    path("board/handcraft/", HandcraftView.as_view()),
    path("board/handcraft/<int:pk>", HandcraftDetailView.as_view()),
    path("board/handcraft/detail/<int:market>/<int:pk>", MarketBoardDetailView.as_view()),
    path("board/group/", GroupView.as_view()),
    path("board/group/<int:pk>", GroupDetailView.as_view()),
    path("board/group/detail/<int:market>/<int:pk>", MarketBoardDetailView.as_view()),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("logout/", logout),
    path("mypage/", MypageView.as_view()),
    path("mypage/update/", MypageUpdateView.as_view()),
    path("mypage/note/", NoteView.as_view()),
    path("mypage/note/read/", ReadNoteView.as_view()),
    path("mypage/note/read/<int:user>/<int:pk>", ReadNoteDetailView.as_view()),
    path("mypage/note/delete/<int:pk>", NoteDeleteView),
    path("notice/", NoticeView.as_view()),
    path("notice/<int:pk>/", NoticeDetailView.as_view()),
    path("notice/admin/", AdminView.as_view()),
    path("notice/admin/authorize/", AuthorizeView.as_view()),
    path("notice/admin/register/", NoticeregisterView.as_view()),
    path("notice/admin/noticemain/", NoticeMainView.as_view()),
    path("notice/admin/talentmarketmain/", TalentMarketMainView.as_view()),
    path("notice/admin/groupmain/", GroupMainView.as_view()),
    path("notice/admin/handcraftmain/", HandcraftMainView.as_view()),
    path("write/<int:pk>", WriteView.as_view()),
    path("ask/qna/", QnaView.as_view()),
    path("ask/answer/", QuestionView.as_view()),
    path("ask/answer/<int:pk>", QuestionDetailView.as_view()),
    path("ask/answer/answer/", AnswerView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path(
        "views/contents/create/<int:pk>",
        ContentCreateView.as_view(),
        name="apis_views_content_create",
    ),
    path(
        "views/market/create/",
        MarketCreateView.as_view(),
        name="apis_views_market_create",
    ),
    path(
        "views/want/create/",
        WantCreateView.as_view(),
        name="apis_views_want_create",
    ),
    path(
        "views/note/create/",
        NoteCreateView.as_view(),
        name="apis_views_note_create",
    ),
    path(
        "views/reply/create/",
        ReplyCreateView.as_view(),
        name="apis_views_reply_create",
    ),
        path(
        "views/comment/create/",
        CommentCreateView.as_view(),
        name="apis_views_comment_create",
    ),
]