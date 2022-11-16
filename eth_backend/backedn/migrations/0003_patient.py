# Generated by Django 4.1.3 on 2022-11-16 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backedn', '0002_remove_doctor_id_alter_doctor_doc_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=100)),
                ('patient_adhaar', models.CharField(max_length=15)),
                ('patient_wallet', models.CharField(max_length=50)),
                ('issue_center', models.CharField(max_length=50)),
            ],
        ),
    ]
