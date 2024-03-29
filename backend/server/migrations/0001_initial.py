# Generated by Django 4.2.4 on 2023-09-01 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('is_mannual', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategies', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='server.game', verbose_name='Game')),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='server.strategy', verbose_name='Strategy')),
            ],
        ),
        migrations.CreateModel(
            name='FrameState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.IntegerField(verbose_name='Frame')),
                ('state', models.JSONField(verbose_name='State')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame_states', to='server.game', verbose_name='Game')),
            ],
        ),
        migrations.CreateModel(
            name='FrameAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame', models.IntegerField(verbose_name='Frame')),
                ('action', models.JSONField(verbose_name='Action')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frame_actions', to='server.player', verbose_name='Player')),
            ],
        ),
    ]
