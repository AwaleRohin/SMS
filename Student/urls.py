from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path('profile/', views.profile, name='profile'),
    path('assignment/', views.assignment, name="assignment"),
    path('newassignment/', views.post_assignment, name="newassignment"),
    # path('<int:pk>/delete/assignment', views.delete_assign, name='delete_assign'),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
    # path('attendance/', views.attendance, name="attendance"),
    # path('attendance/view/', views.attendance_view, name="attendance_view"),
    path('exam/new', views.exam_new, name='add_new_exam'),
    path('exam/', views.exam, name='view_exam'),
    path('course/new', views.course_new, name='add_new_course'),
    path('course/', views.course, name='view_course'),
    path('program/new', views.program_new, name='add_new_program'),
    path('program/', views.program, name='view_program'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
