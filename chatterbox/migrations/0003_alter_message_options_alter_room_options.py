# Generated by Django 4.1.1 on 2022-09-20 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatterbox', '0002_room_host'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
