# Generated by Django 3.2.8 on 2022-01-08 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('phone_no', models.BigIntegerField()),
                ('mail_id', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobcode', models.CharField(max_length=100)),
                ('companyname', models.CharField(max_length=100)),
                ('jobrole', models.CharField(max_length=100)),
                ('dateposted', models.DateField()),
                ('endingdate', models.DateField()),
                ('jobdescription', models.FileField(upload_to='media/')),
                ('appliedcandidates', models.PositiveIntegerField()),
                ('visibility', models.BooleanField(default=False)),
                ('location', models.CharField(max_length=100)),
                ('experience', models.SmallIntegerField()),
                ('salary', models.IntegerField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportalapp.user_account')),
            ],
        ),
        migrations.CreateModel(
            name='AppliedCandidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
                ('phone_no', models.BigIntegerField()),
                ('mail_id', models.CharField(max_length=100)),
                ('jobcode', models.CharField(max_length=100)),
                ('resume', models.FileField(upload_to='resumeMedia/')),
                ('matching', models.FloatField()),
                ('age', models.IntegerField()),
                ('skills', models.CharField(max_length=100)),
                ('experience', models.IntegerField()),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobportalapp.user_account')),
            ],
        ),
    ]
