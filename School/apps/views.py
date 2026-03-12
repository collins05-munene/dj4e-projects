from django.views import View
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Grade, Subject, Teacher

# Create your views here.
class AdminPage(View):
    def get(self, request):
        students = Student.objects.all()
        context = {
            'students': students
        }
        return render(request, 'apps/admin.html', context)
    

class TeacherDetails(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        class_teacher = Grade.objects.all()
        context = {
            'teachers': teachers,
            'class_teacher': class_teacher
        }
        return render(request, 'apps/teacher-details.html', context)
    
class CreateTeacher(View):
    def get(self, request):
        subjects = Subject.objects.all()
        grades = Grade.objects.all()

        context = {'grades': grades, 'subjects': subjects}
        return render(request, 'apps/create-teacher.html', context)
    
    def post(self, request):
        name = request.POST.get('name')
        grade_id = request.POST.get('grade')
        subject_ids = request.POST.getlist('subjects')

        teacher = Teacher.objects.create(name=name)
      
        if subject_ids:
            teacher.subject.set(subject_ids)

        if grade_id:
            grade = Grade.objects.get(id=grade_id)
            grade.teacher = teacher
            grade.save()
        
        return redirect('teacher-details')

    
class CreateStudent(View):
    def get(self, request):
        grades = Grade.objects.all()
        subjects = Subject.objects.all()
        context = {'grades': grades, 'subjects': subjects}
        return render(request, 'apps/create-student.html', context)
    
    def post(self, request):
        #Get form data
        name = request.POST.get('name')
        grade_id = request.POST.get('grade')
        subject_ids = request.POST.getlist('subjects')
        #Create student
        grade = Grade.objects.get(id=grade_id) if grade_id else None
        student = Student.objects.create (
            name=name,
            grade=grade
        )
        #Add many to many fields
        if subject_ids:
            student.subjects.set(subject_ids)

        return redirect('admin-page')

class UpdateStudent(View):
    def get(self, request, adm):
        student = get_object_or_404(Student, adm=adm)
        grades = Grade.objects.all()
        subjects = Subject.objects.all()

        context = {
            'student': student,
            'grades': grades,
            'subjects': subjects
        }
        return render(request, 'apps/update-student.html', context)
    
    def post(self, request, adm):
        student = get_object_or_404(Student, adm=adm)

        student.name = request.POST.get('name')
        grade_id = request.POST.get('grade')

        if grade_id:
            student.grade = Grade.objects.get(id=grade_id)

        student.save()

        subject_ids = request.POST.getlist('subjects')
        student.subjects.set(subject_ids)

        return redirect('admin-page')

class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('admin-page')
    template_name = "apps/student-delete.html"
    pk_url_kwarg = "adm"