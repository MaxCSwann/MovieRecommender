# Generated by Django 2.1.7 on 2019-04-02 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_auto_20190402_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Director',
            field=models.CharField(max_length=100),
        ),
    ]
