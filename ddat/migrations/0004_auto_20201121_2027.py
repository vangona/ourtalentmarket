# Generated by Django 3.1 on 2020-11-21 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddat', '0003_auto_20201121_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='select_name',
            field=models.CharField(default='닉네임', max_length=16, verbose_name='닉네임/실명'),
        ),
    ]