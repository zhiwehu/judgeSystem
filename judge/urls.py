from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from judge import views

urlpatterns = patterns('',
    url(r'^problems/$', views.ProblemList.as_view(), 
        name = 'problem_list'),
   url(r'^problems/page/(?P<page>\d+)/$', views.ProblemList.as_view(), 
       name = 'problem_page'),

   url(r'^problems/new/', 
       permission_required('judge.add_problem')(views.ProblemNew.as_view()), 
       name = 'problem_new'),
   url(r'^problems/(?P<pk>\d+)/edit/$', permission_required(
       'judge.change_problem')(views.ProblemEdit.as_view()), 
       name = 'problem_edit'),

   url(r'^problems/(?P<pk>\d+)/$', views.ProblemDetails.as_view(), 
       name = 'problem_details'),

   url(r'^problems/(?P<problem_id>\d+)/newtest/$', 
       permission_required('judge.add_test')(views.TestNew.as_view()), 
       name = 'test_new'),
   url(r'^test/(?P<pk>\d+)/edit/$', 
       permission_required('judge.change_test')(views.TestEdit.as_view()),
       name = 'test_edit'),

   url(r'^problems/(?P<pk>\d+)/submit/$', 
       login_required(views.SolutionSubmit.as_view()), 
       name = 'solution_submit'),
   url(r'^solutions/(?P<pk>\d+)/$', views.SolutionDetails.as_view(),
       name = 'solution_details'),
)
