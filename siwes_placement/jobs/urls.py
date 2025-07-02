from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-company/', views.add_company, name='add_company'),
    path('add-job/', views.add_job, name='add_job'),
    path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('toggle-job/<int:pk>/', views.toggle_job_status, name='toggle_job_status'),
]