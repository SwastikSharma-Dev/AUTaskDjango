from django.urls import path
from . import views

urlpatterns = [
    path('problem/', views.code_editor, name='code_editor'),
    path('run/', views.run_code, name='run_code'),
]
