# Generated by Django 3.2 on 2021-05-30 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0002_auto_20210529_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_user',
            name='full_name',
            field=models.CharField(default=None, max_length=250, null=True),
        ),
    ]
