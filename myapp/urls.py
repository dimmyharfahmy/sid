# myapp /urls.py
from django.urls import path
from . import views
from .views import custom_logout_view
from django.views.generic import RedirectView

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),  # Root URL for the app
    path('courses/', views.courses_view, name='courses'), # URL for all courses
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('blogs/', views.blog_list, name='blog_list'),  # URL for blog list
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('about/', views.about_view, name='about'),
    path('logout/', custom_logout_view, name='logout'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
