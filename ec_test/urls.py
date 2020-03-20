from django.urls import path
from .views import top_page, item_detail, log_in_page, resister_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', top_page, name='top'),
    path('detail/<int:pk>/', item_detail, name='image_detail'),
    path('login/', log_in_page, name='login'),
    path('resister/', resister_user, name='resister-user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

