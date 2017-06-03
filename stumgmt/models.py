from __future__ import str_literals

from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Student(models.Model):
    # Student Registration Form
    
    # required info
    parent_name = models.CharField(max_length = 100)
    student_name = models.CharField(max_length = 100)
    email_1 = models.EmailField(max_length = 256)
    student_age = models.IntegerField(default = None)
    phone_number_1 = models.CharField(max_length = 20, blank = True, null = True)
    t_and_c = models.BooleanField(default = False)
    
    # Option info
    email_2 = models.EmailField(max_length = 256, blank = True, null = True)
    address = models.CharField(max_length = 256, blank = True, null = True)
    phone_number_2 = models.CharField(max_length = 20, blank = True, null = True)
    preferred_lesson = models.CharField(max_length = 50, blank = True, null = True)
    registration_note = models.TextField(blank = True, null = True)
    
    # for admin use only
    # assign a teacher after student is registered
    teacher = models.ForeignKey('auth.User', blank = True, null = True)
    student_rate = models.IntegerField(default = 0)
    active = models.BooleanField(default = False)
    LOCATION_CHOICES = (
        ('Home', 'Home'),
        ('Studio', 'Studio'),
    )
    
    location = models.CharField(max_length = 10, choices = LOCATION_CHOICES, default = 'Studio')
    student_since = models.DateTimeField(default = timezone.now)
    
    def get_rate(self):
        return self.student_rate
    
    def rate_update(self, new_rate):
        self.student_rate = new_rate
        return self.student_rate
        
    def get_user(self):
        return self.student_name
    
    def __str__(self):
        return self.student_name

class Payment(models.Model):
    
    student = models.ForeignKey(Student, related_name = 'payment')
    # payment received will be manually enetered.
    # the method get_srate() will be used as a reminder
    # for the amount that sould be collected.
    payment_received = models.IntegerField(default = None)
    
    # auto set by django
    payment_date = models.DateTimeField(default = timezone.now)
    PAYMENT_FREQUENCY = (
        ('Monthly', "Monthly"),
        ('Quarterly', "Quarterly"),
        )
    payment_frequency = models.CharField(
        max_length = 15,
        choices = PAYMENT_FREQUENCY,
        default = "Monthly",
        )
    
    next_due_date = models.DateTimeField(blank = True, null = True)
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Check', 'Check'),
        ('Credit Card', 'Credit Card'),
    )
    payment_method =  models.CharField(
        max_length=12,
        choices=PAYMENT_CHOICES,
        default='Cash',
    )
    
    # a method to get Student rate in Student object.
    def get_student_rate(self):
        return self.student.student_rate
    
    def __str__(self):
        return str(self.student.student_name) + ' - $' + str(self.payment_received)
    
    
class Note(models.Model):
    teacher = models.ForeignKey('auth.User', related_name = 'users')
    student = models.ForeignKey(Student, related_name = 'student')
    last_mod_date = models.DateTimeField(default = timezone.now)
    text = models.TextField()
    
    def __str__(self):
        return str(self.teacher)
        
class TeacherLesson(models.Model):
    teacher = models.ForeignKey('auth.User', related_name = 'teacher_lesson')
    student = models.ForeignKey(Student, related_name = 'student_in_teacher')
    
    teacher_confirmation = models.BooleanField(default = False)
    # not visible for modification
    teacher_signed_at = models.DateTimeField(default = timezone.now, blank = True, null = True)
    
    def stash(self):
        self.save()
    
    def __str__(self):
        return str(self.teacher.get_username())

class StudentLesson(models.Model):
    teacher = models.ForeignKey('auth.User', related_name = 'student_lesson')
    student = models.ForeignKey(Student, related_name = 'student_in_student')
    
    student_confirmation = models.BooleanField(default = False)
    # not visible for modification
    student_signed_at = models.DateTimeField(default = timezone.now, blank = True, null = True)
    
    def __str__(self):
        return str(self.student.student_name)
        
class Lesson(models.Model):
    teacher = models.ForeignKey('auth.User', related_name = 'teacher_in_lesson_model')
    student = models.ForeignKey(Student, related_name = 'student_in_lesson_model')
    
    teacher_confirmation = models.BooleanField(default = False)
    
    # not visible for modification
    teacher_signed_at = models.DateTimeField(blank = True, null = True)
    
    student_confirmation = models.BooleanField(default = False)
    student_signed_at = models.DateTimeField(blank = True, null = True)

    def stash(self):
        self.teacher_confirmation = True
        self.teacher_signed_at = timezone.now()
        self.save()    
    
    def __str__(self):
        return str(self.teacher.get_username()) + ' ' + str(self.student.student_name)