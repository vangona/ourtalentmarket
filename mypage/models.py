from django.db import models
from tmuser.models import Tmuser

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=64, verbose_name="쪽지 제목", default="1")
    content = models.TextField(verbose_name="내용", default="1")
    market = models.CharField(
        max_length=64, verbose_name="관련 장/모임 이름", default="", blank=True
    )
    writer = models.ForeignKey(
        Tmuser, on_delete=models.CASCADE, related_name="note_writer", null=True
    )
    receiver = models.ForeignKey(
        Tmuser, on_delete=models.CASCADE, related_name="note_receiver", null=True
    )
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="작성일")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "Note"
        verbose_name = "쪽지"
        verbose_name_plural = "쪽지"