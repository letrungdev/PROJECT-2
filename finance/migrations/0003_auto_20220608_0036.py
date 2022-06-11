# Generated by Django 3.2.9 on 2022-06-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20220607_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='billfold',
            name='billfold_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='billfold',
            name='currency_unit',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='content',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='type',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='billfold',
            name='balance',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='billfold',
            name='inflow',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='billfold',
            name='outflow',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='expenditureplan',
            name='amount',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='expenditureplan',
            name='category',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
