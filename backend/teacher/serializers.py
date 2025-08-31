from rest_framework import serializers
from _applib.model_choice_fields import GenderChoice


class TeacherRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(
        max_length=16,
        regex=r'^(?:\+8801|01)[3-9]\d{8}$',
        error_messages={
            'invalid': 'Enter a valid Bangladeshi phone number (e.g., +8801XXXXXXXXX or 01XXXXXXXXX).'
        }
    )
    full_name = serializers.CharField(max_length=60)
    profile_picture = serializers.CharField(max_length=300)
    gender = serializers.ChoiceField(
        choices=GenderChoice.choices,
        error_messages={
            "err_msg": "Gender must be one of: MALE, FEMALE, OTHER."
        }
    )
    password = serializers.CharField(max_length=30)
