from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('news/', views.announcements_view, name='announcements'),
    path('schedules/', views.schedules_view, name='schedules'),
    path('results/', views.results_view, name='results'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('register/', views.register_view, name='register'), # Nouvelle page
    path('accounts/', include('django.contrib.auth.urls')), # Gère Login/Logout auto
    # ... vos autres urls
]