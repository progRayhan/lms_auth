from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import TeacherModel
from django.contrib.auth.hashers import make_password, check_password


class TeacherRegistrationView(APIView):
    def post(self, request):
        phone = request.data.get("phone_number")
        full_name = request.data.get("full_name")
        profile_picture = request.data.get("profile_picture")
        gender = request.data.get("gender")
        password = make_password(request.data.get("password"))

        TeacherModel.objects.create(
            phone_number=phone,
            full_name=full_name,
            profile_picture=profile_picture,
            gender=gender,
            password=password
        )

        return Response({
            "message": "Success"
        })


class TeacherLoginView(APIView):
    def post(self, request):
        phone = request.data.get("phone_number")
        raw_password = request.data.get("password")

        teacher = TeacherModel.objects.filter(phone_number=phone).last()
        if teacher is None:
            return Response("Teacher not found!")
        
        teacher_hash_pass = teacher.password

        is_pass_valid = check_password(raw_password, teacher_hash_pass)

        if is_pass_valid is True:
            return Response("Password is Valid")
        else:
            return Response("Password is Invalid")
