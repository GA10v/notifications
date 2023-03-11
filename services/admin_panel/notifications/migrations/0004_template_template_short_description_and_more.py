# Generated by Django 4.1.7 on 2023-03-10 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_template_template_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='template_short_description',
            field=models.TextField(
                default='<provide short description for sms and websocket notifications>', verbose_name='template_short'
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='template',
            name='template_content',
            field=models.TextField(verbose_name='template_content'),
        ),
    ]