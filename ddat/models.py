import os
import uuid
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from tmuser.models import Tmuser

# Create your models here.
def image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class Market(models.Model):
    UPLOAD_PATH = "user-upload"

    admin = models.ForeignKey(Tmuser, on_delete=models.CASCADE, null=True)

    market_name = models.CharField(max_length=32, verbose_name="장/모임 이름", default="기본값")

    index_name = models.CharField(max_length=64, verbose_name="분류", default="기본값")

    content = models.TextField(verbose_name="설명")

    image = models.ImageField(upload_to=image_upload_to, blank=True)

    image_thumbnail = ImageSpecField(
        source="image", processors=[ResizeToFill(200, 150)]
    )

    user = models.ManyToManyField(Tmuser, related_name="user", blank=True)

    authorization = models.CharField(max_length=4, verbose_name="승인 여부", default="N")

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    modified_dttm = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    def __str__(self):
        return self.market_name

    class Meta:
        db_table = "our_talent_market"
        verbose_name = "만들고자 하는 재능장"
        verbose_name_plural = "만들고자 하는 재능장"


class Wants(models.Model):
    admin = models.ForeignKey(Tmuser, on_delete=models.CASCADE, null=True)

    summary = models.CharField(max_length=32, verbose_name="한 줄 요약", default="기본값")

    index_name_w = models.CharField(max_length=64, verbose_name="분류", default="기본값")

    content_w = models.TextField(verbose_name="설명")

    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    modified_dttm = models.DateTimeField(auto_now=True, verbose_name="수정시간")

    def __str__(self):
        return self.summary

    class Meta:
        db_table = "our_talent_market_wants"
        verbose_name = "원하는 재능장"
        verbose_name_plural = "원하는 재능장"