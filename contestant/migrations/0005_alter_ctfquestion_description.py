# Generated by Django 4.2.17 on 2025-02-14 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contestant', '0004_ctfquestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctfquestion',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
    ]
