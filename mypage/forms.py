from django import forms


class MypageUpdateForm(forms.Form):
    usernickname = forms.CharField(label="닉네임", required=False)

    phonenumber = forms.CharField(label="연락처", required=False)

    def clean(self):
        cleaned_data = super().clean()
        usernickname = cleaned_data.get("usernickname")
        phonenumber = cleaned_data.get("phonenumber")


class IdVerificationForm(forms.Form):
    id_image = forms.ImageField(label="학생증 사진", required=False)

    def clean(self):
        cleaned_data = super().clean()
        id_image = cleaned_data.get("id_image")
