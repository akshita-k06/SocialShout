# Generated by Django 3.2 on 2021-06-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0011_alter_complaint_subcategory_servant_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_user',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
