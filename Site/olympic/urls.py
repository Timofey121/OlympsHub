from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', main, name='home'),
    path('account/', account, name='account'),

    path('olympiads/', all_olympiads, name='olympiads'),
    path('olympiads/<slug:subject_slug>/', filter_olympiads, name='subject'),

    path('notifications/', notification_management, name='notifications'),
    path('change_email/', change_email, name='change_email'),

    path('telegram_token/', telegram_token, name='telegram_token'),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/<slug:token>', password_reset_for_user, name='password_reset_for_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
