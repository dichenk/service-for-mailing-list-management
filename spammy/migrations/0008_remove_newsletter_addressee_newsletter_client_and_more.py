# Generated by Django 4.1.6 on 2023-02-05 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spammy', '0007_alter_newslettersystem_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='addressee',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='client',
            field=models.ManyToManyField(to='spammy.client', verbose_name='Адресат'),
        ),
        migrations.DeleteModel(
            name='NewsletterSystem',
        ),
    ]
