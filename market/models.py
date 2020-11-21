import os
import uuid
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from ddat.models import Market
from tmuser.models import Tmuser

# Create your models here.
def image_upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return os.path.join(instance.UPLOAD_PATH, "%s.%s" % (uuid.uuid4(), ext))


class TalentMarket(Market):
    def __str__(self):
        return self.market_name

    class Meta:
        db_table = "talent_market"
        verbose_name = "재능장"
        verbose_name_plural = "재능장"


class Group(Market):
    def __str__(self):
        return self.market_name

    class Meta:
        db_table = "group"
        verbose_name = "소모임"
        verbose_name_plural = "소모임"


class Handcraft(Market):
    def __str__(self):
        return self.market_name

    class Meta:
        db_table = "handcraft"
        verbose_name = "공예품장"
        verbose_name_plural = "공예품장"

