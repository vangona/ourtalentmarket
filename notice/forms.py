from django import forms
from .models import NoticeModel
from ddat.models import Market


class NoticeregisterForm(forms.Form):
    title = forms.CharField(error_messages={"required": "제목을 입력해주세요."}, label="공지 제목")
    image = forms.ImageField(required=False)
    content = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="공지 내용")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")


class AuthorizeForm(forms.Form):
    market_name = forms.CharField(
        error_messages={"required": "장/모임 이름을 선택해주세요."}, label="장/모임 이름"
    )
    authorization = forms.CharField(
        error_messages={"required": "승인여부를 확인해주세요."}, label="승인 여부"
    )

    def clean(self):
        cleaned_data = super().clean()
        market_name = cleaned_data.get("market_name")
        authorization = cleaned_data.get("authorization")


class NoticeMainForm(forms.Form):
    title = forms.CharField(error_messages={"required": "장/모임 이름을 선택해주세요."}, label="제목")
    main = forms.CharField(error_messages={"required": "승인여부를 확인해주세요."}, label="메인 공지")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        main = cleaned_data.get("main")


class MarketMainForm(forms.Form):
    market_name = forms.CharField(
        error_messages={"required": "장/모임 이름을 선택해주세요."}, label="제목"
    )
    main = forms.CharField(error_messages={"required": "승인여부를 확인해주세요."}, label="메인 공지")

    main_content = forms.CharField(
        error_messages={"required": "메인 내용을 입력해주세요."}, label="메인 내용"
    )

    def clean(self):
        cleaned_data = super().clean()
        market_name = cleaned_data.get("market_name")
        main = cleaned_data.get("main")
        main_content = cleaned_data.get("main_content")
