from django import forms
from .models import Content, Questions, Answer


class WritingForm(forms.Form):
    title = forms.CharField(
        error_messages={"required": "제목을 입력해주세요."}, max_length=64, label="글 제목"
    )
    image = forms.ImageField(required=False)
    description = forms.CharField(
        error_messages={"required": "내용을 입력해주세요."}, label="내용"
    )

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        image = cleaned_data.get("image")
        description = cleaned_data.get("description")


class QuestionForm(forms.Form):
    title = forms.CharField(
        error_messages={"required": "제목을 입력해주세요."}, label="질문 제목"
    )
    content = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="질문 내용")

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")


class AnswerForm(forms.Form):
    question = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="질문")

    title = forms.CharField(
        error_messages={"required": "제목을 입력해주세요."}, max_length=64, label="답변 제목"
    )
    content = forms.CharField(error_messages={"required": "내용을 입력해주세요."}, label="답변 내용")

    def clean(self):
        cleaned_data = super().clean()
        question = cleaned_data.get("question")
        title = cleaned_data.get("title")
        content = cleaned_data.get("content")
