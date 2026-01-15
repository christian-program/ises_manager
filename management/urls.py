
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('create/', views.create_post, name='create_post'),
    path('bulk-upload/', views.bulk_upload, name='bulk_upload'),
]