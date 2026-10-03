from rest_framework import serializers
from django.conf import settings

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        students = attrs.get('students', [])

        if len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError(f"На курсе не может быть более {settings.MAX_STUDENTS_PER_COURSE} студентов!")

        return attrs
