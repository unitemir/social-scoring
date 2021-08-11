# Generated by Django 3.2 on 2021-08-11 09:11

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_person_social_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='mainapp.person', verbose_name='Родитель'),
        ),
        migrations.AddField(
            model_name='person',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='score',
            field=models.FloatField(default=1, verbose_name='Рейтинг'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='username',
            field=models.CharField(default=1, max_length=128, verbose_name='Имя пользователя'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='avg_amount_likes_on_all_posts',
            field=models.FloatField(blank=True, null=True, verbose_name='Среднее количество лайков на всех постах'),
        ),
        migrations.AlterField(
            model_name='person',
            name='avg_amount_likes_on_last_20_posts',
            field=models.FloatField(blank=True, null=True, verbose_name='Среднее количество лайков на последних 20 постах'),
        ),
        migrations.AlterField(
            model_name='person',
            name='qty_posts',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество постов'),
        ),
        migrations.AlterField(
            model_name='person',
            name='qty_subscribers',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество подписчиков'),
        ),
        migrations.AlterField(
            model_name='person',
            name='subscriptions',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество подписок'),
        ),
    ]
