# Generated by Django 3.2.9 on 2022-06-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_alter_track_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='time',
        ),
        migrations.AddField(
            model_name='track',
            name='time_track',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
