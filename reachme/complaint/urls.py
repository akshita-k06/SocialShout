from django.urls import path, include
from . import views

urlpatterns = [
   path('dashboard/', views.dashboard, name="dashboard"),  
   path('update/complaint/tracker/', views.updateComplaint, name="updateComplaint"),  
]
