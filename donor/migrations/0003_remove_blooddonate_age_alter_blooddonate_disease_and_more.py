# Generated by Django 4.1.7 on 2023-03-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0002_alter_blooddonate_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blooddonate',
            name='age',
        ),
        migrations.AlterField(
            model_name='blooddonate',
            name='disease',
            field=models.CharField(default='Nil', max_length=100),
        ),
        migrations.AlterField(
            model_name='blooddonate',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')], default='pending', max_length=20),
        ),
    ]
