from django.urls import path
from .views import CreateDynamicTableModel, UpdateDynamicTableModel, GetAllRows

urlpatterns = [
    path('table', CreateDynamicTableModel.as_view(), name='create-dynamic-table'),
    path('table/<str:id>', UpdateDynamicTableModel.as_view(), name='update-dynamic-table'),
    path('table/<str:id>/row', GetAllRows.as_view(actions={'post': 'create'}), name='create-table-row'),
    path('table/<str:id>/rows', GetAllRows.as_view(actions={'get': 'list'}), name='get-all-table-rows'),
]
