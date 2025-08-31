from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
import requests
import json
from .models import TeacherModel
from django.contrib.auth.hashers import make_password, check_password
from .serializers import TeacherRegistrationSerializer
from _applib.model_choice_fields import TeacherStatus


class TeacherRegistrationView(APIView):
    def send_otp(self):
        # project auth
        # url otp
        url = "http://127.0.0.1:8000/otp/send/"

        payload = {
            "otp_for": "phone",
            "identifier": self.request.data.get("phone_number"),
            "reason": "activate_account"
        }

        requests.post(url, data=payload)
    
    def post(self, request):
        postman_data = request.data
        register_serializer = TeacherRegistrationSerializer(data=postman_data)
        is_serializer_valid = register_serializer.is_valid()

        teacher_exist = TeacherModel.objects.filter(
            phone_number=register_serializer.validated_data.get("phone_number")
            ).exists()
        if teacher_exist is True:
            return Response({
                "msg": "Phone number already exist",
                "data": {}
            })

        if is_serializer_valid is True:
            TeacherModel.objects.create(
                phone_number=register_serializer.validated_data.get("phone_number"),
                full_name=register_serializer.validated_data.get("full_name"),
                profile_picture=register_serializer.validated_data.get("profile_picture"),
                gender=register_serializer.validated_data.get("gender"),
                password=register_serializer.validated_data.get("password")
            )
            # send otp sms
            self.send_otp()
            
            return Response({
                "msg": "Success",
                "data": register_serializer.validated_data
            })
        else:
            return Response({
                "msg": "Failed",
                "data": register_serializer.errors
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


class TeacherApproveView(APIView):
    def patch(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        payload = {
            "phone_number": phone_number,
            "otp": otp
        }
        
        verify_otp = requests.post(
            url="http://127.0.0.1:8000/otp/verify/",
            data=payload
        )

        verify_otp_data = verify_otp.json()
        is_otp_valid = verify_otp_data.get("is_valid")

        if is_otp_valid is True:
            teacher = TeacherModel.objects.filter(phone_number=phone_number).last()
            teacher.status = TeacherStatus.APPROVED
            teacher.gender = "FEMALE"
            teacher.save()
            return Response("Teacher has been updated")
        else:
            data = {
                "msg": "Teacher does not updated",
                "reason": verify_otp_data.get("msg")
            }
            return Response(data)


