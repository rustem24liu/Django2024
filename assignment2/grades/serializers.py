from rest_framework import serializers
from .models import Grade
from courses.models import Course, Enrollment
from students.models import Student


# from ..courses.models import Course


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    # teacher_name = serializers.CharField(source='teacher.username', read_only=True)

    class Meta:
        model = Grade
        fields = [ 'student', 'student_name', 'course', 'course_name', 'grade', 'date']
        read_only_fields = ['student_name', 'course_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.groups.filter(name='Teacher').exists():
            self.fields['course'].queryset = Course.objects.filter(instructor=request.user)
            self.fields['student'].queryset = Student.objects.filter(
                enrollment__course__in=self.fields['course'].queryset
            )

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        course = data['course']

        course = data.get('course')
        print(f'Course is :{course}')

        if not course:
            raise serializers.ValidationError("Course is required.")

        if course.instructor != user:
            raise serializers.ValidationError("You can only grade students in courses you teach!")
        student = data['student']

        if not Enrollment.objects.filter(course=course, student=student).exists():
            raise serializers.ValidationError("This student is not enrolled in the selected course!")

        return data

class StudentCoursesGradeSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    grade_letter = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ['course_name', 'grade', 'grade_letter']

    def get_grade_letter(self, obj):
        if obj.grade >= 90:
            return "A"
        elif obj.grade >= 80:
            return "B+"
        elif obj.grade >= 70:
            return "B"
        elif obj.grade >= 60:
            return "C"
        else:
            return "F"