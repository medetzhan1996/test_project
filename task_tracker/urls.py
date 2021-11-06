from django.urls import path
from . import views
app_name = 'task_tracker'
urlpatterns = [
    path('task/list', views.TaskListView.as_view(),
         name="task_list"),
    path('task/create', views.TaskFormView.as_view(), name="task_create"),
    path('task/<int:pk>/update', views.TaskFormView.as_view(),
         name="task_update"),
]
