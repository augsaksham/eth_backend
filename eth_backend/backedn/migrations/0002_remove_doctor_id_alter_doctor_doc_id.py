# Generated by Django 4.1.3 on 2022-11-16 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backedn', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='id',
        ),
        migrations.AlterField(
            model_name='doctor',
            name='doc_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]