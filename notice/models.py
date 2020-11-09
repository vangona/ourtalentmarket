import os
import uuid
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from market.models import TalentMarket, Group, Handcraft

# Create your models here.
def image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class NoticeModel(models.Model):
    UPLOAD_PATH = "user-upload"

    title = models.CharField(max_length=32, verbose_name="제목")

    image = models.ImageField(upload_to=image_upload_to, blank=True)

    image_thumbnail = ImageSpecField(
        source="image", processors=[ResizeToFill(600, 480)]
    )

    content = models.TextField(verbose_name="공지 내용")

    writer = models.CharField(
        max_length=8,
        verbose_name="작성자",
    )

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    modified_dttm = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notice"
        verbose_name = "공지사항"
        verbose_name_plural = "공지사항"


class MainModel(models.Model):
    notice = models.ForeignKey(
        NoticeModel,
        on_delete=models.CASCADE,
        related_name="notice",
        null=True,
        blank=True,
    )

    talentmarket = models.ForeignKey(
        TalentMarket,
        on_delete=models.CASCADE,
        related_name="talentmarket",
        null=True,
        blank=True,
    )

    talentmarket_main = models.TextField(verbose_name="재능장 메인 설명", default="기본값")

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="group",
        null=True,
        blank=True,
    )

    group_main = models.TextField(verbose_name="소모임 메인 설명", default="기본값")

    handcraft = models.ForeignKey(
        Handcraft,
        on_delete=models.CASCADE,
        related_name="handcraft",
        blank=True,
        null=True,
    )

    handcraft_main = models.TextField(verbose_name="소공예품 메인 설명", default="기본값")

    def __str__(self):
        return self.talentmarket_main

    class Meta:
        db_table = "main"
        verbose_name = "게시판 메인"
        verbose_name_plural = "게시판 메인"