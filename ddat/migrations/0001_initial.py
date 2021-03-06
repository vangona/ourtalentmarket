# Generated by Django 3.1 on 2020-11-06 15:17

import ddat.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tmuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(default='기본값', max_length=32, verbose_name='한 줄 요약')),
                ('index_name_w', models.CharField(default='기본값', max_length=64, verbose_name='분류')),
                ('content_w', models.TextField(verbose_name='설명')),
                ('registered_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('modified_dttm', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tmuser.tmuser')),
            ],
            options={
                'verbose_name': '원하는 재능장',
                'verbose_name_plural': '원하는 재능장',
                'db_table': 'our_talent_market_wants',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_name', models.CharField(default='기본값', max_length=32, verbose_name='장/모임 이름')),
                ('index_name', models.CharField(default='기본값', max_length=64, verbose_name='분류')),
                ('content', models.TextField(verbose_name='설명')),
                ('image', models.ImageField(blank=True, upload_to=ddat.models.image_upload_to)),
                ('authorization', models.CharField(default='N', max_length=4, verbose_name='승인 여부')),
                ('registered_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('modified_dttm', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tmuser.tmuser')),
                ('user', models.ManyToManyField(null=True, related_name='user', to='tmuser.Tmuser')),
            ],
            options={
                'verbose_name': '만들고자 하는 재능장',
                'verbose_name_plural': '만들고자 하는 재능장',
                'db_table': 'our_talent_market',
            },
        ),
    ]
