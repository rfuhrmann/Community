# Generated by Django 2.1.2 on 2018-11-06 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Discussion Title', max_length=254)),
                ('message', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discussion_Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='Message')),
                ('date', models.DateField(auto_now=True)),
                ('discussion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='discussions.Discussion')),
            ],
        ),
    ]
