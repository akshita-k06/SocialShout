# Generated by Django 3.2 on 2021-06-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0007_complaint_subcategory_servant_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_subcategory',
            name='servant_role',
            field=models.SmallIntegerField(choices=[(1, 'MSEB Chief Engineer'), (2, 'Municipal Commissioner'), (3, 'Water Conservation officer'), (4, 'Public grievance officer'), (5, 'Department Safety Officer')], default=0),
        ),
    ]
