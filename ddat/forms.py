from django import forms
from .models import Market, Wants


class MarketForm(forms.Form):
    market_name = forms.CharField(
        error_messages={"required": "제목을 입력해주세요."}, max_length=32, label="장/모임 이름"
    )
    index_name = forms.CharField(
        error_messages={"required": "분류를 선택해주세요."}, max_length=64, label="분류"
    )
    image = forms.ImageField(
        error_messages={"required": "대표사진을 설정해주세요."}, label="대표 사진"
    )
    content = forms.CharField(error_messages={"required": "설명을 입력해주세요."}, label="설명")

    def clean(self):
        cleaned_data = super().clean()
        market_name = cleaned_data.get("market_name")
        index_name = cleaned_data.get("index_name")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")

        if not (market_name and index_name and image and content):
            self.add_error("market_name", "값이 없습니다.")
            self.add_error("index_name", "값이 없습니다.")
            self.add_error("image", "값이 없습니다.")
            self.add_error("content", "값이 없습니다.")


class WantsForm(forms.Form):
    summary = forms.CharField(
        error_messages={"required": "한 줄 요약을 입력해주세요."}, label="한 줄 요약"
    )
    index_name_w = forms.CharField(
        error_messages={"required": "분류를 선택해주세요."}, label="분류"
    )
    content_w = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="내용")

    def clean(self):
        cleaned_data = super().clean()
        summary = cleaned_data.get("summary")
        index_name_w = cleaned_data.get("index_name_w")
        content_w = cleaned_data.get("content_w")

        if not (summary and index_name_w and content_w):
            self.add_error("summary", "값이 없습니다.")
            self.add_error("index_name_w", "값이 없습니다.")
            self.add_error("content_w", "값이 없습니다.")