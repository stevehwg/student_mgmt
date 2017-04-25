# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-18 03:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_mod_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_received', models.IntegerField(default=0)),
                ('payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_frequency', models.CharField(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly')], default='Monthly', max_length=15)),
                ('next_due_date', models.DateTimeField(blank=True, null=True)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Check', 'Check'), ('Credit Card', 'Credit Card')], default='Cash', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_name', models.CharField(max_length=100)),
                ('student_name', models.CharField(max_length=100)),
                ('email_1', models.EmailField(max_length=256)),
                ('student_age', models.IntegerField(default=0)),
                ('phone_number_1', models.CharField(blank=True, max_length=20, null=True)),
                ('t_and_c', models.BooleanField(default=False)),
                ('email_2', models.EmailField(blank=True, max_length=256, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('phone_number_2', models.CharField(blank=True, max_length=20, null=True)),
                ('preferred_lesson', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_note', models.TextField(blank=True, null=True)),
                ('student_rate', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('location', models.CharField(choices=[('Home', 'Home'), ('Studio', 'Studio')], default='Studio', max_length=10)),
                ('student_since', models.DateTimeField(default=django.utils.timezone.now)),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_confirmation', models.BooleanField(default=False)),
                ('student_signed_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_in_student', to='stumgmt.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_lesson', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherLesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_confirmation', models.BooleanField(default=False)),
                ('teacher_signed_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_in_teacher', to='stumgmt.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_lesson', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='stumgmt.Student'),
        ),
        migrations.AddField(
            model_name='note',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='stumgmt.Student'),
        ),
        migrations.AddField(
            model_name='note',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
