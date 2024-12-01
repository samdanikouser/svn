# Generated by Django 5.1.3 on 2024-11-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('line_staff', 'Line Staff'), ('supervisors', 'Supervisors'), ('managers', 'Managers'), ('e_learning', 'e-Learning')], max_length=50, null=True),
        ),
    ]
