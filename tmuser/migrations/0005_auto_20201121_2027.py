# Generated by Django 3.1 on 2020-11-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tmuser', '0004_auto_20201121_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmuser',
            name='id_verification',
            field=models.CharField(default='X', max_length=4, verbose_name='학생증 인증 여부'),
        ),
    ]
