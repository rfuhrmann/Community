# Generated by Django 2.1.2 on 2018-11-06 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181106_1407'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status_comment',
            old_name='Status',
            new_name='status',
        ),
    ]
