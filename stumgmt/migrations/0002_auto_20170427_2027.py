# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 03:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stumgmt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_confirmation', models.BooleanField(default=False)),
                ('student_confirmation', models.BooleanField(default=False)),
                ('teacher_signed_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('student_signed_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_received',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_age',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_in_lesson_model', to='stumgmt.Student'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_in_lesson_model', to=settings.AUTH_USER_MODEL),
        ),
    ]