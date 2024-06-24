"""
URL configuration for ecomgk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path


# manual importing start
from django.conf import settings
from django.conf.urls.static import static
# manual importing end

urlpatterns = [
    path('admin/', admin.site.urls), # comment this when u do migrate after makeMigrations
    path("", include("core.urls")),
    path("user/", include("userauths.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")), # when we install django-ckeditor, vo aap hi directory or file "ckeditor_uploader" bna deta hai
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # manually added urls
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #####################
else:
    import django.views.static
    # debug = false lyi urlPatterns iss trah pass kride aa
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
        re_path(r'^media/(?P<path>.*)$', django.views.static.serve,
                {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG})
    ]

print("ggn 40", urlpatterns)
