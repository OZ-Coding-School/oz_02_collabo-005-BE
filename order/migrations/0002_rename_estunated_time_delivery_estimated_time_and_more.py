# Generated by Django 5.0.4 on 2024-05-03 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='estunated_time',
            new_name='estimated_time',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, 'Order received'), (1, 'Cooking'), (2, 'Cooking complete')]),
        ),
    ]