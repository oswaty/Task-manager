from django.urls import path
from . import views

app_name="tasks"
urlpatterns = [
    path('',views.index,name='index'),
    path('register',views.register, name='register'),
    path('login',views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('task_list',views.task_list,name="task_list"),
    path('tasks/<int:pk>',views.task_detail,name="task_detail"),
    path('task_create',views.task_create,name='task_create')

 ]
 