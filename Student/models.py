from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your models here.

SEMESTER = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
)

LEVELS = (
    ('Bachelor', 'Bachelor'),
    ('Master', 'Master'),
)

ATTENDANCE = (
    ('Present', 'Present'),
    ('Absent', 'Absent'),
)


class Program(models.Model):
    name = models.CharField(max_length=150)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField(max_length=600, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    credits = models.IntegerField(null=True, default=0)
    semester = models.IntegerField(choices=SEMESTER, default=1)
    level = models.CharField(max_length=100, choices=LEVELS, default='Bachelor')

    def __str__(self):
        return self.name


# class User(AbstractUser):
#     is_student = models.BooleanField('student status', default=False)
#     is_teacher = models.BooleanField('teacher status', default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    picture = models.ImageField(upload_to='profile_pic', null=True, blank=True, default='no-img.png')
    email = models.EmailField(max_length=100, null=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    course = models.ManyToManyField(Course, related_name='course', blank=True)
    semester = models.IntegerField(choices=SEMESTER, default=1)
    level = models.CharField(max_length=100, choices=LEVELS, default='Bachelor')

    def __str__(self):
        if self.first_name and not self.last_name:
            return self.first_name
        elif self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return 'Student'


def create_profile(sender, **kwargs):
    if kwargs['created']:
        student = Student.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile, sender=User)


class Assignment(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx','ppt', 'pptx', 'zip', 'rar', '7zip', 'txt', 'csv'])])
    upload_time = models.DateTimeField(default=datetime.now, null=True)
    due_date = models.DateField(null=True)

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'

    def __str__(self):
        return str(self.name)


# class Attendance(models.Model):
#     student = models.ManyToManyField(Student, related_name='student', blank=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     status = models.CharField(max_length=100, choices=ATTENDANCE, default='Present')
#     date = models.DateField(default=datetime.now, null=True)
#
#     def __str__(self):
#         return str(self.date) + ' (' + str(self.course) + ')'
    #
    # def save(self, *args, **kwargs):
    #     if self.course not in self.student.course:
    #         raise ValidationError("Can't register attendance of student not enrolled in course")
    #     super().save(*args, **kwargs)


class Exam(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name)
