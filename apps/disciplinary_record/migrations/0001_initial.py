# Generated by Django 3.2.6 on 2024-12-14 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_auto_20241208_1633'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DisciplinaryRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('issues_realted_to', models.CharField(blank=True, max_length=200, null=True)),
                ('incident_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('inspector_signature', models.TextField(blank=True, null=True)),
                ('employee_signature', models.TextField(blank=True, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_disciplinary_record_updates', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplinary_record_employee', to='authentication.userprofile')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_disciplinary_record_updates', to=settings.AUTH_USER_MODEL)),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='disciplinary_record_inspector', to='authentication.userprofile')),
            ],
        ),
    ]
