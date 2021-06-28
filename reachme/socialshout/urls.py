from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('problems/',views.problems,name="problms"),
    path('problems/subproblems/<int:subproblem_id>',views.subproblems,name="subproblems"),
    path('problems/subproblems/registration/<int:problem_id>/<str:problem>/<int:subproblem_id>/<str:subproblem>',views.registration,name="registration"),
    path('regform/<int:problem_id>/<str:problem>/<int:subproblem_id>/<str:subproblem>', views.regform, name="regform"),
    path('verify/',views.verify,name="verify"),
   path('tracker/', views.tracker, name="tracker"),  
]
