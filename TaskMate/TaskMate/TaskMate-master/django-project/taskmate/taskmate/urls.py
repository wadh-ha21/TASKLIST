
from django.contrib import admin
from django.urls import path, include
from todolist_app import views as todolist_views
from todolist_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', todolist_views.index, name='index'),

    path('todolist/',include('todolist_app.urls')),
    path('account/',include('users_app.urls')),
    path('contact', todolist_views.contact, name='contact'),
    path('about',todolist_views.about, name='about'),
    path('api/tasks/', views.api_get_tasks, name='api_get_tasks'),  # GET all tasks
    path('api/task/<int:task_id>/', views.api_get_task, name='api_get_task'),  # GET a single task
    path('api/task/create/', views.api_create_task, name='api_create_task'),  # POST to create a task
    path('api/task/update/<int:task_id>/', views.api_update_task, name='api_update_task'),  # PUT to update a task
    path('api/task/delete/<int:task_id>/', views.api_delete_task, name='api_delete_task'),  # DELETE a task
       
]
