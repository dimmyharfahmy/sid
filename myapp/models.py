from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    content = CKEditor5Field('Content')

    class Meta:
        verbose_name = "My model"
        verbose_name_plural = "My models"

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='author_images/')
    course_image = models.ImageField(upload_to='course_images/')
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    status = models.CharField(max_length=10)  # OPEN or CLOSED
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    lectures = models.IntegerField()
    enrolled_students = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    certificate = models.BooleanField(default=False)
    curriculum = models.CharField(max_length=255, default="Default Curriculum")
    start_date = models.DateTimeField(null=True, blank=True)  # Tanggal

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Course)
def resize_course_image(sender, instance, **kwargs):
    if instance.course_image:
        img = Image.open(instance.course_image)
        desired_width = 320
        desired_height = 320
        img.thumbnail((desired_width, desired_height), Image.LANCZOS)
        img.save(instance.course_image.path)


# class Enrollment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     enrolled_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Enrollment"
#         verbose_name_plural = "Enrollments"

#     def __str__(self):
#         return f"{self.user.username} enrolled in {self.course.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

    def user_email(self):
        return self.user.email
    user_email.short_description = 'User Email'


class Author(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='author_images/')

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = CKEditor5Field('Content', config_name='default')
    publish_date = models.DateField()
    likes = models.IntegerField(default=0)
    tags = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog_images/')

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Blog)
def resize_blog_image(sender, instance, **kwargs):
    if instance.image:
        img = Image.open(instance.image)
        desired_width = 330
        desired_height = 220
        img.thumbnail((desired_width, desired_height), Image.LANCZOS)
        img.save(instance.image.path)

class Testimonial(models.Model):
    testi_name = models.CharField(max_length=100)
    testi_designation = models.CharField(max_length=100)
    testi_image = models.ImageField(upload_to='author_images/')
    testi_rating = models.PositiveIntegerField(default=0)
    testi_content = models.TextField()

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.testi_name
