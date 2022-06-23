from django.urls import path
from .views import main_page, statistic, test_control, image_control, ipconfig, monitoring, table_config
from .views import brightness_control
from .services import CreateStand, DeleteStand, UpdateStand, delete_image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('images/', image_control,  name='images'),
    path('images/<int:pk>/', delete_image, name='delete_image'),
    path('brightness/', brightness_control, name='brightness'),
    path('ajax/crud/create/', CreateStand.as_view(), name='crud_ajax_create'),
    path('ajax/crud/delete/', DeleteStand.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/update/', UpdateStand.as_view(), name='crud_ajax_update'),
    path('statistic/', statistic, name='statistic'),
    path('test/', test_control, name='test'),
    path('ipconfig/', ipconfig, name='ipconfig'),
    path('table_config/', table_config, name='table_config'),
    path('', main_page, name='main'),
    path('main-monitoring/', monitoring, name='main_monitoring'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


