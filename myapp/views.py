# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm, CustomUserCreationForm  
from .models import Contact, Enrollment, Course, Blog, Testimonial
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from datetime import datetime
import logging

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully.')
            form = ContactForm()  # Reset form after successful submission
    else:
        form = ContactForm()
    return render(request, 'myapp/contact.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print("Form is not valid")  # Debugging
            print(form.errors)  # Debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def register_view(request):
    return render(request, 'myapp/register.html')

logger = logging.getLogger(__name__)

@csrf_protect
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

# def login_view(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'myapp/login.html', {'form': form})


def home(request):
    from django.utils import timezone

    courses = Course.objects.all().order_by('-id')[:3]  # Fetch the 3 most recent courses
    latest_blogs = Blog.objects.order_by('-publish_date')[:3]
    testimonials = Testimonial.objects.all()  # Fetch all testimonials

    now = timezone.now()  # Get the current time as an aware datetime object

    for course in courses:
        if course.status == "OPEN" and course.start_date:
            # Ensure course.start_date is also aware
            if timezone.is_naive(course.start_date):
                course_start_date = timezone.make_aware(course.start_date)
            else:
                course_start_date = course.start_date

            course.countdown = (course_start_date - now).days
        else:
            course.countdown = None

    context = {
        'courses': courses,
        'latest_blogs': latest_blogs,
        'testimonials': testimonials
    }
    return render(request, 'myapp/home.html', context)

def custom_logout_view(request):
    logout(request)
    return redirect('home')

def courses_view(request):
    now = timezone.now()  # Get the current time as an aware datetime object

    # Get all courses ordered by start_date descending
    all_courses = Course.objects.all().order_by('-start_date')

    for course in all_courses:
        if course.status == "OPEN" and course.start_date:
            # Ensure course.start_date is also aware
            if timezone.is_naive(course.start_date):
                course_start_date = timezone.make_aware(course.start_date)
            else:
                course_start_date = course.start_date

            course.countdown = (course_start_date - now).days
        else:
            course.countdown = None

    context = {'courses': all_courses}
    return render(request, 'myapp/courses.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {'course': course}
    return render(request, 'myapp/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    # Check if the course is closed
    if course.status == "CLOSED":
        messages.error(request, 'This course is already closed.')
        return redirect('course_detail', course_id=course_id)

    # Check if the user is already enrolled
    if not Enrollment.objects.filter(user=user, course=course).exists():
        # Create a new enrollment
        Enrollment.objects.create(user=user, course=course)
        messages.success(request, f'You have successfully enrolled in {course.title}')
    else:
        messages.info(request, f'You are already enrolled in {course.title}')
    
    return redirect('course_detail', course_id=course_id)

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    recent_blogs = Blog.objects.order_by('-publish_date')[:4]
    context = {
        'blog': blog,
        'recent_blogs': recent_blogs
    }
    return render(request, 'myapp/blog_detail.html', context)

def blog_list(request):
    blogs = Blog.objects.all()
    recent_blogs = Blog.objects.order_by('-publish_date')[:4]
    context = {
        'blogs': blogs,
        'recent_blogs': recent_blogs
    }
    return render(request, 'myapp/blog_list.html', context)

def about_view(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'myapp/about.html', {'testimonials': testimonials})

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def robots_txt(_):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /login/",
        "Disallow: /media/",
        "Disallow: /static/",
        "Disallow: /settings/",
        "Disallow: /account/",
        "Disallow: /password_reset/",
        "Allow: /",
        "Sitemap: https://sidfoundation.or.id/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")