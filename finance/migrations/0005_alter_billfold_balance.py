# Generated by Django 3.2.9 on 2022-06-08 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_alter_transaction_tran_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billfold',
            name='balance',
            field=models.IntegerField(null=True),
        ),
    ]
