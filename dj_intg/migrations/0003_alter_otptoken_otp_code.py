# Generated by Django 5.0.6 on 2024-06-25 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_intg', '0002_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='0cc99e', max_length=6),
        ),
    ]
