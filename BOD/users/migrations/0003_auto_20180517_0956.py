# Generated by Django 2.0.3 on 2018-05-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180516_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinfo',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectmanager',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
