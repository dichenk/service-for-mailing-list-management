# Generated by Django 4.1.6 on 2023-02-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spammy', '0004_alter_client_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='comment',
            field=models.TextField(null=True, verbose_name='Комментарий'),
        ),
    ]