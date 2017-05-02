from django.contrib import admin

# Register your models here.
from .models import Student, Payment, Note, TeacherLesson, StudentLesson, Lesson

admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(Note)
admin.site.register(TeacherLesson)
admin.site.register(StudentLesson)
admin.site.register(Lesson)