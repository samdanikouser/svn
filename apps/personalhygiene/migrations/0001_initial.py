# Generated by Django 3.2.6 on 2024-12-03 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0006_alter_userprofile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='personal_hygiene_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalHygiene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('inspected_date', models.DateField(blank=True, null=True)),
                ('parameters_checked', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_hygiene_employee', to='authentication.userprofile')),
                ('inspected_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_hygiene_inspector', to='authentication.userprofile')),
                ('photos', models.ManyToManyField(blank=True, to='personalhygiene.UploadedPhoto')),
            ],
        ),
    ]