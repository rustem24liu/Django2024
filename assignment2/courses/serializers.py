from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *
from students.models import Student

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    # print(f'Instructor name is the{instructor_name}..')
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor' ,'instructor_name']

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    instructor_name = serializers.CharField(source='instructor.user.username', read_only=True)


    class Meta:
        model = Enrollment
        fields =['id' , 'student','student_name', 'course', 'course_name', 'instructor_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.user.groups.filter(name='Student').exists():
            self.fields.pop('student')

        elif request and request.user.is_staff:
            self.fields['student'].queryset = Student.objects.all()
            self.fields['course'].queryset = Course.objects.all()

    def validate(self, data):
        request = self.context.get('request')
        course = data.get('course')

        if Enrollment.objects.filter(student=request.user.student, course=course).exists():
            raise serializers.ValidationError('You are already enrolled this course')

        if request.user.groups.filter(name='Student').exists() and course.instructor == request.user:
            raise serializers.ValidationError('You cannot enroll in courses you teach')
        return data


class TeacherSelectionSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['instructor', 'instructor_name', 'course',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        course = self.context.get('course')
        if course:
            self.fields['instructor'].queryset = User.objects.filter(courses__id=course.id, groups__name="Teacher")

            enrollment = self.instance
            if enrollment and enrollment.instructor:
                self.fields['instructor'].initial = enrollment.instructor

    def update(self, instance, validated_data):
        validated_data.pop('student', None)
        validated_data.pop('course', None)
        return super().update(instance, validated_data)

    def validate(self, data):
        course = data['course']
        teacher = data['instructor']

        if teacher != course.instructor:
            raise serializers.ValidationError("You can only choose a teacher who is the instructor of the course.")

        return data
