# Generated by Django 2.0 on 2019-07-08 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20190708_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[('sz', '深圳'), ('bj', '北京'), ('sh', '上海')], max_length=64),
        ),
    ]
