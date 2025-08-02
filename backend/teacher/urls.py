from django.urls import path
from .views import TeacherRegistrationView, TeacherLoginView

urlpatterns = [
    # http://127.0.0.1:8000/teacher/register/
    path(
        route="register/",
        view=TeacherRegistrationView.as_view(),
        name="teacher_register"
    ),
    # http://127.0.0.1:8000/teacher/login/
    path(
        route="login/",
        view=TeacherLoginView.as_view(),
        name="teacher_login"
    )
]