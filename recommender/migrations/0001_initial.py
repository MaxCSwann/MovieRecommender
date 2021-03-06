# Generated by Django 2.1.5 on 2019-03-07 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(default='', editable=False, max_length=40)),
                ('Genre', models.CharField(max_length=40)),
                ('Director', models.CharField(max_length=60)),
                ('Actors', models.TextField()),
                ('Plot', models.TextField()),
                ('tomatoURL', models.URLField()),
                ('Poster', models.URLField()),
            ],
        ),
    ]
