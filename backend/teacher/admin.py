from django.contrib import admin
from .models import TeacherModel

@admin.register(TeacherModel)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "full_name",
        "gender",
        "status",
        "created_at",
        "updated_at",
    )
