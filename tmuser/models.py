import os
import uuid
from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail, ResizeToFit
# Create your models here.


def image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class Tmuser(models.Model):
    UPLOAD_PATH = "user-upload"

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

# 추가된 부분

    id_verification = models.CharField(
        max_length=4, verbose_name="학생증 인증 여부", default="X")

    id_image = ProcessedImageField(
        upload_to=image_upload_to,
        processors=[ResizeToFit(width=2048, upscale=False)],
        format='JPEG',
        options={'quality': 70},
        blank=True,
        verbose_name="학생증 사진")

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


class WaitingId(models.Model):
    waiting_user = models.ForeignKey(
        Tmuser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.waiting_user.username

    class Meta:
        db_table = "waiting_id"
        verbose_name = "승인대기중인 학생증"
        verbose_name_plural = "승인대기중인 학생증"
