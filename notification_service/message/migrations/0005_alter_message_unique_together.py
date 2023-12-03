# Generated by Django 4.2.7 on 2023-12-03 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_tag'),
        ('newsletter', '0001_initial'),
        ('message', '0004_alter_message_newsletter_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='message',
            unique_together={('newsletter_id', 'user_id')},
        ),
    ]