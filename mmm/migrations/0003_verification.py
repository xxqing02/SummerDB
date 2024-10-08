# Generated by Django 5.0.6 on 2024-07-24 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmm', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('code', models.CharField(max_length=6, null=True)),
                ('expiresAt', models.DateTimeField(null=True)),
            ],
        ),
    ]
