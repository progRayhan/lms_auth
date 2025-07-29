from django.db import models
from _applib.model_choice_fields import GenderChoice, TeacherStatus


class TeacherModel(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=60)
    profile_picture = models.CharField(max_length=300)
    gender = models.CharField(max_length=10, choices=GenderChoice.choices, default=GenderChoice.MALE)
    website = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=15, choices=TeacherStatus.choices, default=TeacherStatus.PENDING)
    password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FullName: {self.full_name} || phone number: {self.phone_number} || status: {self.status}"
    
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        db_table = "teacher"
