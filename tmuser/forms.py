from django import forms
from django.contrib.auth.hashers import check_password
from .models import Tmuser


class RegisterForm(forms.Form):
    private = forms.CharField(
        error_messages={"required": "개인정보 수집 동의에 체크해주세요."},
        max_length=4,
        label="개인정보 수집 동의",
    )

    useremail = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )

    usernickname = forms.CharField(
        error_messages={"required": "닉네임을 입력해주세요."}, max_length=32, label="닉네임"
    )

    password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )
    re_password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호 확인",
    )

    username = forms.CharField(
        error_messages={"required": "이름을 입력해주세요."}, max_length=32, label="이름"
    )

    phonenumber = forms.CharField(
        error_messages={"required": "연락처를 입력해주세요."}, max_length=16, label="연락처"
    )

    department_name = forms.CharField(
        error_messages={"required": "학과를 입력해주세요."}, max_length=64, label="학과"
    )

    student_number = forms.CharField(
        error_messages={"required": "학번을 입력해주세요."}, max_length=8, label="학번"
    )

    def clean(self):
        cleaned_data = super().clean()
        private = cleaned_data.get("private")
        useremail = cleaned_data.get("useremail")
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")
        username = cleaned_data.get("username")
        usernickname = cleaned_data.get("usernickname")
        phonenumber = cleaned_data.get("phonenumber")
        department_name = cleaned_data.get("department_name")
        student_number = cleaned_data.get("student_number")

        if Tmuser.objects.all() == None:
            if Tmuser.objects.get(useremail=useremail) != None:
                self.add_error("useremail", "같은 이메일이 가입되어 있습니다.")

            if private != "Y":
                self.add_error("private", "개인정보 수집 동의에 거부 하셨습니다.")

            if password and re_password:
                if password != re_password:
                    self.add_error("password", "비밀번호가 서로 다릅니다.")
                    self.add_error("re_password", "비밀번호가 서로 다릅니다.")

            if len(student_number) != 8:
                self.add_error("student_number", "올바른 학번을 입력해주세요.")

        else:
            if private != "Y":
                self.add_error("private", "개인정보 수집 동의에 거부 하셨습니다.")

            if password and re_password:
                if password != re_password:
                    self.add_error("password", "비밀번호가 서로 다릅니다.")
                    self.add_error("re_password", "비밀번호가 서로 다릅니다.")

            if len(student_number) != 8:
                self.add_error("student_number", "올바른 학번을 입력해주세요.")


class LoginForm(forms.Form):
    useremail = forms.EmailField(
        error_messages={"required": "이메일을 입력해주세요."}, max_length=64, label="이메일"
    )
    password = forms.CharField(
        error_messages={"required": "비밀번호를 입력해주세요."},
        widget=forms.PasswordInput,
        label="비밀번호",
    )

    def clean(self):
        cleaned_data = super().clean()
        useremail = cleaned_data.get("useremail")
        password = cleaned_data.get("password")

        if useremail and password:
            try:
                tmuser = Tmuser.objects.get(useremail=useremail)
            except Tmuser.DoesNotExist:
                self.add_error("useremail", "아이디가 없습니다.")
                return

            if not check_password(password, tmuser.password):
                self.add_error("password", "비밀번호가 틀렸습니다.")
