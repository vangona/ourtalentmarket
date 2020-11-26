# Generated by Django 3.1 on 2020-11-21 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tmuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmuser',
            name='id_verification',
            field=models.CharField(default='N', max_length=4, verbose_name='학생증 인증 여부'),
        ),
        migrations.CreateModel(
            name='WaitingId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waiting_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tmuser.tmuser')),
            ],
            options={
                'verbose_name': '승인대기중인 학생증',
                'verbose_name_plural': '승인대기중인 학생증',
                'db_table': 'waiting_id',
            },
        ),
    ]