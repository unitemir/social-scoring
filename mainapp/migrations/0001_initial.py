# Generated by Django 3.2 on 2021-08-26 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie_json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_username', models.CharField(max_length=128, verbose_name='USERNAME')),
            ],
        ),
        migrations.CreateModel(
            name='InstagramAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='PersonStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_subscribers', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество подписчиков')),
                ('subscriptions', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество подписок')),
                ('qty_posts', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество постов')),
                ('avg_amount_likes_on_all_posts', models.FloatField(blank=True, null=True, verbose_name='Среднее количество лайков на всех постах')),
                ('avg_amount_likes_on_last_20_posts', models.FloatField(blank=True, null=True, verbose_name='Среднее количество лайков на последних 20 постах')),
            ],
        ),
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128, verbose_name='ФИО')),
                ('score', models.FloatField(blank=True, null=True, verbose_name='Рейтинг')),
                ('stats', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.personstats')),
            ],
        ),
    ]
