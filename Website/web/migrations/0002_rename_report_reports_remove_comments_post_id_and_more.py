# Generated by Django 5.1.3 on 2024-11-29 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='Reports',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='web.post'),
        ),
    ]
