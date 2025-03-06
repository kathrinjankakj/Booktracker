import profile

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from gallery import views
from gallery.views import overview, upload, user_settings, profile

urlpatterns = [
    path('', overview, name='overview'),
    path('upload', upload, name='upload'),
    path('user_settings', user_settings, name='user_settings'),
    path('profile', profile, name='profile'),
    path('update_progress/<int:book_id>/', views.update_progress, name='update_progress'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
