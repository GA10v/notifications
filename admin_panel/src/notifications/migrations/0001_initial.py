# Generated by Django 3.2 on 2023-01-10 20:33

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: list = []

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_id', models.UUIDField(db_index=True)),
                (
                    'content_type',
                    models.CharField(
                        choices=[
                            ('new_film', 'New Film'),
                            ('new_user', 'New User'),
                            ('review_like', 'Review Like'),
                            ('custom', 'Custom Mail'),
                        ],
                        max_length=15,
                    ),
                ),
                ('content', models.JSONField()),
            ],
            options={
                'db_table': 'content',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                (
                    'notification_id',
                    models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                ('content_id', models.UUIDField(db_index=True)),
                (
                    'content_type',
                    models.CharField(
                        choices=[
                            ('new_film', 'New Film'),
                            ('new_user', 'New User'),
                            ('review_like', 'Review Like'),
                            ('custom', 'Custom Mail'),
                        ],
                        max_length=15,
                    ),
                ),
                ('last_update', models.DateTimeField(auto_now=True, null=True)),
                ('last_notification_send', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'notification',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(db_index=True)),
                ('notification_id', models.UUIDField(db_index=True)),
                ('last_notification_send_to_user', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'subscription',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(db_index=True)),
                (
                    'communication_method',
                    models.CharField(
                        choices=[('ws', 'Ws'), ('email', 'Email'), ('telegram', 'Telegram')], max_length=15
                    ),
                ),
                ('allow_communication', models.BooleanField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddConstraint(
            model_name='notification',
            constraint=models.UniqueConstraint(fields=('content_id', 'content_type'), name='idx_notification'),
        ),
        migrations.AddConstraint(
            model_name='content',
            constraint=models.UniqueConstraint(fields=('content_id', 'content_type'), name='idx_content'),
        ),
        migrations.CreateModel(
            name='CustomMail',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('notifications.content',),
        ),
        migrations.CreateModel(
            name='NewEpisodeMail',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('notifications.content',),
        ),
    ]
