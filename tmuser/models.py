from django.db import models
# Create your models here.


class Tmuser(models.Model):
    private = models.CharField(max_length=4, verbose_name="개인정보 수집 동의")

    useremail = models.EmailField(max_length=128, verbose_name="이메일")

    password = models.CharField(max_length=128, verbose_name="비밀번호")

    level = models.CharField(
        max_length=8,
        verbose_name="등급",
    )

    username = models.CharField(max_length=32, verbose_name="이름")

    usernickname = models.CharField(max_length=32, verbose_name="닉네임")

    phonenumber = models.CharField(max_length=16, verbose_name="연락처")

    department_name = models.CharField(max_length=64, verbose_name="학과")

    student_number = models.CharField(max_length=8, verbose_name="학번")

    registered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name="등록시간"
    )

    modified_dttm = models.DateTimeField(
        auto_now=True, verbose_name="수정시간"
    )    

    def __str__(self):
        return self.usernickname

    class Meta:
        db_table = "talent_market_users"
        verbose_name = "재능장 사용자"
        verbose_name_plural = "재능장 사용자"
