# Generated by Django 2.1.2 on 2018-11-20 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussions', '0003_auto_20181106_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='status',
            field=models.CharField(default='open', max_length=50),
        ),
    ]
