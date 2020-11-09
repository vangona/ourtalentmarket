from django import forms
from ddat.models import Market


# class MarketRegisterForm(forms.Form):
#     market_name = forms.CharField(
#         error_messages={"required": "장/모임 이름을 입력해주세요."}, label="장/모임 이름"
#     )
#     index_name = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="분류")
#     image = forms.ImageField(
#         error_messages={"required": "대표사진을 설정해주세요."}, label="대표 사진"
#     )
#     content = forms.CharField(
#         error_messages={"required": "장/모임에 대한 설명을 입력해주세요."}, label="설명"
#     )

#     def clean(self):
#         cleaned_data = super().clean()
#         market_name = cleaned_data.get("market_name")
#         index_name = cleaned_data.get("index_name")
#         image = cleaned_data.get("image")
#         content = cleaned_data.get("content")


class MarketUpdateForm(forms.Form):
    market_name = forms.CharField(label="장/모임 이름", required=False)
    image = forms.ImageField(label="대표 사진", required=False)
    content = forms.CharField(label="설명", required=False)

    def clean(self):
        cleaned_data = super().clean()
        market_name = cleaned_data.get("market_name")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")