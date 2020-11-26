from django import forms
from .models import Market, Wants


class MarketForm(forms.Form):
    market_name = forms.CharField(
        error_messages={"required": "제목을 입력해주세요."}, max_length=32, label="장/모임 이름"
    )
    campus = forms.CharField(
        error_messages={"required": "캠퍼스를 선택해주세요."},
        label="캠퍼스 구분")
    index_name = forms.CharField(
        error_messages={"required": "분류를 선택해주세요."}, max_length=64, label="분류"
    )
    image = forms.ImageField(
        error_messages={"required": "대표사진을 설정해주세요."}, label="대표 사진"
    )
    content = forms.CharField(
        error_messages={"required": "설명을 입력해주세요."}, label="설명")

    def clean(self):
        cleaned_data = super().clean()
        market_name = cleaned_data.get("market_name")
        index_name = cleaned_data.get("index_name")
        campus = cleaned_data.get("campus")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")

        if not (market_name):
            self.add_error("market_name", "장/모임 이름을 입력해주세요.")

        if not image:
            self.add_error("image", "대표사진이 없습니다.")

        if not index_name:
            self.add_error("index_name", "분류가 선택되지 않았습니다.")

        if not campus:
            self.add_error("campus", "캠퍼스가 선택되지 않았습니다.")

        if not content:
            self.add_error("content", "설명이 입력되지 않았습니다.")

        try:
            Market.objects.get(market_name=market_name)
            self.add_error("market_name", "동일한 장/모임 이름이 존재합니다.")

        except:
            pass


class WantsForm(forms.Form):
    summary = forms.CharField(
        error_messages={"required": "한 줄 요약을 입력해주세요."}, label="한 줄 요약"
    )
    index_name_w = forms.CharField(
        error_messages={"required": "분류를 선택해주세요."}, label="분류"
    )
    content_w = forms.CharField(
        error_messages={"required": "내용을 입력해주세요."}, label="내용")

    def clean(self):
        cleaned_data = super().clean()
        summary = cleaned_data.get("summary")
        index_name_w = cleaned_data.get("index_name_w")
        content_w = cleaned_data.get("content_w")

        if not summary:
            self.add_error("summary", "한 줄 요약이 없습니다.")

        if not index_name_w:
            self.add_error("index_name_w", "분류가 선택되지 않았습니다.")

        if not content_w:
            self.add_error("content_w", "설명이 입력되지 않았습니다.")

        else:
            pass
