from django import forms
from .models import Student, Payment, TeacherLesson, StudentLesson, Lesson

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = (
            'parent_name',
            'student_name',
            'student_age',
            'email_1',
            'phone_number_1',
            'preferred_lesson',
            'location',
            't_and_c',
            'registration_note',
            )

class PaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        fields = (
            'student',
            'payment_received',
            'payment_frequency',
            'payment_method',
            )

class TeacherLessonForm(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = (
            'teacher',
            'student',
            'teacher_confirmation',
            )
            
class StudentLessonForm(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = (
            'teacher',
            'student',
            'student_confirmation',
            )
            
class SearchForm(forms.Form):
    search = forms.CharField(max_length = 50)