# Generated by Django 5.1.3 on 2024-11-10 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_gen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='musictrack',
            name='error_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='musictrack',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
