# Generated by Django 4.1.7 on 2023-03-07 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_template_options_alter_template_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='template_files',
            field=models.FilePathField(allow_files=False, allow_folders=True, default='', path='templates/'),
            preserve_default=False,
        ),
    ]
