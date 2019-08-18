# Generated by Django 2.1.2 on 2018-12-04 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20181204_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.IntegerField(choices=[(1, 'Other'), (2, 'Sport'), (3, 'Party'), (4, 'Food'), (5, 'Work'), (6, 'Meeting'), (7, 'Sauna'), (8, 'Family'), (9, 'SitSit')], max_length=254),
        ),
    ]
