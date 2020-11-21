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
    market_for_update = forms.CharField(label="수정할 장/모임 이름", required=False)
    market_name = forms.CharField(label="장/모임 이름 수정", required=False)
    image = forms.ImageField(label="대표 사진", required=False)
    content = forms.CharField(label="설명", required=False)

    def clean(self):
        cleaned_data = super().clean()
        market_for_update = cleaned_data.get("market_for_update")
        market_name = cleaned_data.get("market_name")
        image = cleaned_data.get("image")
        content = cleaned_data.get("content")

        try :
            Market.objects.get(market_name=market_name)
            self.add_error("market_name", "동일한 장/모임 이름이 존재합니다.")

        except:
            return

        if market_name == "" :
            self.add_error("market_name", "장/모임 이름을 입력해주세요.")

class MarketBoardUpdateForm(forms.Form):
    title = forms.CharField(label="게시글 제목", required=False)
    content = forms.CharField(label="내용", required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
