# Generated by Django 4.2.14 on 2024-08-08 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_comment_created_at_alter_comment_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='test',
            new_name='text',
        ),
    ]
