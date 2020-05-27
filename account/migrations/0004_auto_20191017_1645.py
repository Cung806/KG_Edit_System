# Generated by Django 2.2.5 on 2019-10-17 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageDomain', '0001_initial'),
        ('account', '0003_auto_20191009_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_role',
        ),
        migrations.AddField(
            model_name='user',
            name='user_domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='manageDomain.DomainModel'),
            preserve_default=False,
        ),
    ]