# myproject/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Only one include statement for myapp.urls
    path('', include('myapp.urls')),  # Delegating root URL to myapp.urls
    path('debug/', include('debug_toolbar.urls', namespace='debug_toolbar')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Serve media files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


