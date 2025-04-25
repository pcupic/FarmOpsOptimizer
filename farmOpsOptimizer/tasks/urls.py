from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('create/', views.create_task, name='create_task'),
    path('list/', views.task_list, name='task_list'),  
    path('edit/<int:id>/', views.edit_task, name='task_edit'),
    path('delete/<int:id>/', views.delete_task, name='task_delete'),
]
