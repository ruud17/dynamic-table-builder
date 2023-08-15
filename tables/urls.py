from django.urls import path
from .views import DynamicTableGenerationView

urlpatterns = [
    path('api/tables', DynamicTableGenerationView.as_view(), name='table-generation'),
]
