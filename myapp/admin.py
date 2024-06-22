from django.contrib import admin
from .models import Contact, MyModel, Course, Blog, Author, Testimonial, Enrollment
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

# Form khusus untuk menggunakan CKEditor5Widget
class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Blog
        fields = '__all__'

# ModelAdmin khusus yang menggunakan BlogAdminForm
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'content')
    search_fields = ('name',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'course', 'enrolled_at')
    search_fields = ('user__username', 'user__email', 'course__title')
    list_filter = ('enrolled_at',)
    ordering = ('-enrolled_at',)

# Mendaftarkan model Blog dengan BlogAdmin
admin.site.register(Blog, BlogAdmin)

# Mendaftarkan model lainnya
admin.site.register(Course)
admin.site.register(Testimonial)
admin.site.register(Author)
