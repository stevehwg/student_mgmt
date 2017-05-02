from django.shortcuts import render, get_object_or_404, redirect
from .models import Student,Payment, Note, TeacherLesson, StudentLesson, Lesson
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import get_template
from django.contrib.auth.models import User
from .forms import StudentForm, PaymentForm, TeacherLessonForm, StudentLessonForm, SearchForm

# from django.views.generic import ListView # Import if using class based views
# Create your views here.

def index(request):
	# student_list = Student.objects.order_by('-student_rate')
	
	if request.method == 'POST':
		form = StudentForm(request.POST, prefix='student')

		if form.is_valid():
			student = form.save(commit = False)

			#Email alert for comment
			# context = {'name': comment.post, 'sender': comment.author, 'message': comment.text} 
			# template = get_template('blog/contact_temp.txt')
			# content = template.render(context)

			# # Compose email message
			# email = EmailMessage('A New Student Registered', content, 'sh19238 contact', to=['Steven Hwang <shihwei.hwang@gmail.com>'])
			# email.send()

			student.save()
			return redirect('index')
	else:
		form = StudentForm(prefix='student')
	
	# search form NOT WORKING
	# if request.method == 'POST':
	# 	searchform = SearchForm(request.POST, prefix='search')

	# 	if searchform.is_valid():
	# 		search_query = searchform.cleaned_data['q']
	# 		search_result = Student.objects.filter(student_name=search_query)

	# 		#Email alert for comment
	# 		# context = {'name': comment.post, 'sender': comment.author, 'message': comment.text} 
	# 		# template = get_template('blog/contact_temp.txt')
	# 		# content = template.render(context)

	# 		# # Compose email message
	# 		# email = EmailMessage('A New Student Registered', content, 'sh19238 contact', to=['Steven Hwang <shihwei.hwang@gmail.com>'])
	# 		# email.send()

	# 		context = {'query': search_result}
	# 		return render(request, 'stumgmt/searchresult.html', context)
	# else:
	# 	searchform = SearchForm(prefix='search')
	
	searchform = SearchForm(prefix='search')
	
	context = {'form': form, 'search': searchform,}
	
	return render(request, 'stumgmt/index.html', context)

def payment(request, **pk):
	
	try:
		student = get_object_or_404(Student, pk=pk['pk'])
		default_data = {
			'student': student,
			}
	except:
		pass
	
	if request.method == 'POST':
		
		form = PaymentForm(request.POST)

		if form.is_valid():
			payment = form.save(commit = False)
			if payment.payment_frequency == 'Quarterly':
				payment.next_due_date = timezone.now() + timezone.timedelta(days = 7*7)
			else:
				payment.next_due_date = timezone.now() + timezone.timedelta(days = 21)
			
			try:
				student.student = student
			except:
				pass


			#Email alert for comment
			# context = {'name': comment.post, 'sender': comment.author, 'message': comment.text} 
			# template = get_template('blog/contact_temp.txt')
			# content = template.render(context)

			# # Compose email message
			# email = EmailMessage('Comment from sh19238 website', content, 'sh19238 contact', to=['Steven Hwang <shihwei.hwang@gmail.com>'])
			# email.send()
			student.active = True
			student.save()
			payment.save()
			return redirect('student_list')
	else:
		
		try:
			form = PaymentForm(initial=default_data)
		except:
			form = PaymentForm()
		
	try:
		context = {'form': form, 'student': student}
	except:
		context = {'form': form}
	
	# return rendered data
	return render(request, 'stumgmt/payment.html', context)	

def teacher_lesson(request, **pk):

	try:
		lesson = get_object_or_404(Lesson, pk=pk['pk'])
		student = lesson.student
		student_o = get_object_or_404(Student, pk=student.pk)
		default_data = {
			'student': student_o,
			}
	except:
		pass
	
	if request.method == 'POST':
		form = TeacherLessonForm(request.POST, instance=lesson)

		if form.is_valid():
			confirm = form.save(commit = False)
			# student.post = post
			# student.author = request.user


			confirm.stash()
			return redirect('index')
	else:
		try:
			form = TeacherLessonForm(initial=default_data)
		except:
			form = TeacherLessonForm()

	
	try:
		context = {'form': form, 'student': student_o}
	except:
		context = {'form': form}
	
	return render(request, 'stumgmt/lesson.html', context)	

def student_lesson(request, **pk):
	
	try:
		student = get_object_or_404(Student, pk=pk['pk'])
		lesson = student.student_in_lesson_model.all()
		default_data = {
			'student': student,
			
			}
	except:
		pass
	
	if request.method == 'POST':
		form = StudentLessonForm(request.POST)

		if form.is_valid():
			confirm = form.save(commit = False)
			# student.post = post
			# student.author = request.user

			#Email alert for comment
			# context = {'name': comment.post, 'sender': comment.author, 'message': comment.text} 
			# template = get_template('blog/contact_temp.txt')
			# content = template.render(context)

			# # Compose email message
			# email = EmailMessage('Comment from sh19238 website', content, 'sh19238 contact', to=['Steven Hwang <shihwei.hwang@gmail.com>'])
			# email.send()
			confirm.student_signed_at = timezone.now()
			confirm.save()
			return redirect('index')
	else:
		
		try:
			form = StudentLessonForm(initial=default_data)
		except:
			form = StudentLessonForm()
	
	context = {'form': form}
	return render(request, 'stumgmt/student_lesson.html', context)	

def student_list(request):
	student_list = Student.objects.all()
	context = {'student_list': student_list}
	return render(request, 'stumgmt/student_list.html', context)

def student_detail(request, pk):
	student = get_object_or_404(Student, pk=pk)
	unsigned = Lesson.objects.filter(student = student, teacher_signed_at__isnull = True).order_by('-student_signed_at')
	context = {'student': student, 'unsigned': unsigned}
	return render(request, 'stumgmt/student_detail.html', context)


def search_result(request, *view_limit):
	
	try:
		view_limit = request.GET.get('view_limit')
	except:
		pass

	query_string = request.GET.get('q')
	query = Student.objects.filter(student_name__icontains=query_string)
	
	#Pagination
	try:
		paginator = Paginator(query, view_limit, orphans=1)
	except:
		paginator = Paginator(query, 2, orphans=1)
		
	page = request.GET.get('page')
	
	try:
		query = paginator.page(page)
	except PageNotAnInteger:
		query = paginator.page(1)
	except EmptyPage:
		query = paginator.page(paginator.num_pages)
		
	# path = request.get_full_path()
	# referer = request.META.get('HTTP_REFERER')
	# new_p = referer+path[1:]+'?q='+query_string
	context = {'query_string': query_string, 'query': query, 'view_limit': view_limit}
	
	# try:
	# 	return redirect('search', query_string, view_limit)
	# except:

	return render(request, 'stumgmt/search_result.html', context)
    
# class Student_List(ListView):
	
# 	model = Student
# 	# return student_list.html
# 	# or return using template_name = 'name.html'
# 	template_name = 'stumgmt/student_list.html'
	
# 	def get_context_data(self, **kwargs):
# 		context = super(Student_List, self).get_context_data(**kwargs)
# 		return context