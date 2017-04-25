from django.conf.urls import url
from . import views 

urlpatterns = [
	# Index landing page
	# url(r'^$', views.Index.as_view(), name = 'index'),
	url(r'^$', views.index, name='index'),
	url(r'^record_payment/$', views.payment, name='new_payment'),
	url(r'^record_payment/(?P<pk>[0-9]+)/$', views.payment, name='new_student_payment'),
	url(r'^record_lesson/$', views.teacher_lesson, name='teacher_lesson'),
	url(r'^student_lesson/$', views.student_lesson, name='student_lesson'),
	url(r'^students/$', views.student_list, name='student_list'),
	url(r'^students/(?P<pk>[0-9]+)/$', views.student_detail, name='student_detail'),
	url(r'^search/$', views.search_result, name='search'),
]
