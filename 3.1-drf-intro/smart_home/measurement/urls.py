from django.urls import path
from .views import SensorView, MeasurementCreateView, SensorsListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorsListView.as_view()),
    path('sensors/<int:pk>/', SensorView.as_view()),
    path('sensors/<int:pk>/measurements/', MeasurementCreateView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)