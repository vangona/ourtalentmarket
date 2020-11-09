import os
import uuid
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from tmuser.models import Tmuser
from ddat.models import Market

# Create your models here.
class Questions(models.Model):
    username = models.CharField(max_length=32, verbose_name="이름")

    usernickname = models.CharField(max_length=32, verbose_name="닉네임")

    useremail = models.EmailField(max_length=128, verbose_name="이메일")

    phonenumber = models.CharField(max_length=16, verbose_name="연락처", default="기본값")

    department_name = models.CharField(max_length=64, verbose_name="학과")

    student_number = models.CharField(max_length=8, verbose_name="학번")

    title = models.CharField(max_length=32, verbose_name="제목")

    content = models.TextField(verbose_name="질문 내용")

    answered = models.CharField(max_length=4, verbose_name="답변 여부", default="N")

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    modified_dttm = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "questions"
        verbose_name = "사용자 문의사항"
        verbose_name_plural = "사용자 문의사항"


class Answer(models.Model):
    question = models.ForeignKey(
        Questions, on_delete=models.CASCADE, related_name="answer", null=True
    )

    title = models.CharField(max_length=32, verbose_name="답변 제목")

    content = models.TextField(verbose_name="답변 내용")

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "answer"
        verbose_name = "문의 답변"
        verbose_name_plural = "문의 답변"


class Content(models.Model):
    title = models.CharField(max_length=64, verbose_name="제목")

    description = models.TextField(verbose_name="설명", default="")

    writer = models.CharField(max_length=8, verbose_name="작성자")

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    modified_dttm = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content"
        verbose_name = "내용"
        verbose_name_plural = "내용"


def image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class Image(models.Model):
    UPLOAD_PATH = "user-upload"

    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)
    image_thumbnail = ImageSpecField(
        source="image", processors=[ResizeToFill(200, 150)]
    )
    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="board", null=True
    )
    order = models.SmallIntegerField()

    class Meta:
        ordering = ["order"]