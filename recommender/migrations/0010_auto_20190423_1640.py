# Generated by Django 2.1.5 on 2019-04-23 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0009_member_answers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('name', 'image')},
        ),
    ]