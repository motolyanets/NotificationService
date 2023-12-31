# Generated by Django 4.2.7 on 2023-11-27 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('in progress', 'In progress'), ('delivered', 'Delivered'), ('is not delivered', 'Is not delivered')])),
                ('client_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.user')),
                ('newsletter_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='newsletter.newsletter')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
