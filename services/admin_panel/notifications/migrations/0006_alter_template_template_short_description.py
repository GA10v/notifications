# Generated by Django 4.1.7 on 2023-03-10 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_alter_template_template_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='template_short_description',
            field=models.TextField(verbose_name='short_description'),
        ),
    ]