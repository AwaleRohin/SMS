from django.contrib import admin
from .models import Student, Course, Program, Assignment, Exam

# Register your models here.


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Assignment)
admin.site.register(Exam)

