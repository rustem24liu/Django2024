from rest_framework import serializers
from .models import Attendance
from courses.models import Enrollment
from students.models import Student


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 'date', 'status']
        read_only_fields = ['course']  # Course is automatically set and cannot be modified

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Restrict the students list to those enrolled in the selected course
        request = self.context.get('request')
        if request:
            course_id = request.parser_context['kwargs'].get('course_id')
            if course_id:
                enrolled_students = Enrollment.objects.filter(course_id=course_id).values_list('student', flat=True)
                self.fields['student'].queryset = Student.objects.filter(id__in=enrolled_students)
