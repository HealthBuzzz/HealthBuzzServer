# Generated by Django 3.1.3 on 2020-12-04 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buzz', '0003_auto_20201123_0137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='today_ranking',
            new_name='today_ranking_stretch',
        ),
        migrations.AddField(
            model_name='profile',
            name='today_ranking_water',
            field=models.IntegerField(default=100),
        ),
    ]
