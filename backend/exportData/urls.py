from django.urls import path
from .views import ExportView, ExportFieldsView

urlpatterns = [
    path('fields/', ExportFieldsView.as_view(), name='export-fields-api'),
    path('', ExportView.as_view(), name='export-api'),
]
