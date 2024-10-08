from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

tm = 'registration/registration_form.html'

urlpatterns = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/registration/',
         CreateView.as_view(template_name=tm,
                            form_class=UserCreationForm,
                            success_url=reverse_lazy('blog:index')),
         name='registration'),
    path('auth/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
