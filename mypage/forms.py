from django import forms


class MypageUpdateForm(forms.Form):
    usernickname = forms.CharField(label="닉네임", required=False)

    phonenumber = forms.CharField(label="연락처", required=False)

    def clean(self):
        cleaned_data = super().clean()
        usernickname = cleaned_data.get("usernickname")
        phonenumber = cleaned_data.get("phonenumber")