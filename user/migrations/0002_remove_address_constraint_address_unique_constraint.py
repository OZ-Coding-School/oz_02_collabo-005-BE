# Generated by Django 5.0.4 on 2024-05-02 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='address',
            name='constraint',
        ),
        migrations.AddConstraint(
            model_name='address',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_constraint'),
        ),
    ]