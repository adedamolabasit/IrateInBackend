# Generated by Django 5.0 on 2024-01-05 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='initiator',
            field=models.IntegerField(default=0),
        ),
    ]
