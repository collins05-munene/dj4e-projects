from django.views import View
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Grade, Subject, Teacher
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = { 'form': form}
        return render(request, 'apps/login.html', context)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin-page')
            elif hasattr(user, 'teacher'):
                return redirect('teacher-dashboard')
            else:
                return redirect('login')
        else:
            context = {
                "error": 'Invalid username or password'
            }
            return render(request, 'apps/login.html', context)
class AdminPage(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return render(self.request, 'apps.not-authorized.html')
    
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
    
class UpdateTeacher(View):
    def get(self, request, id):
        teacher = get_object_or_404(Teacher, id=id)
        subjects = Subject.objects.all()
        grades = Grade.objects.all()

        context = {
            'teacher': teacher,
            'subjects': subjects,
            'grades': grades
        }
        return render(request, 'apps/update-teacher.html', context)
    
    def post(self, request, id):
        teacher = get_object_or_404(Teacher, id=id)

        teacher.name = request.POST.get('name')
        teacher.save()
        grade_id = request.POST.get('grade')
        subject_ids = request.POST.getlist('subjects')

        Grade.objects.filter(teacher=teacher).update(teacher=None)
        if grade_id:
            grade = Grade.objects.get(id=grade_id)
            grade.teacher = teacher
            grade.save()


        if subject_ids:
            teacher.subject.set(subject_ids)

        return redirect('teacher-details')

class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher-details')
    template_name = "apps/delete-teacher.html"
    pk_url_kwarg = "id"

    
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

class TeacherDashboard(LoginRequiredMixin, View):
    def get(self, request):
        teacher = request.user.teacher
        classes = Grade.objects.filter(teacher=teacher)
        students =Student.objects.filter(grade__teacher=teacher)
        subjects = teacher.subject.all()

        context = {
            'classes': classes,
            'students': students,
            'subjects': subjects
        }

        return render(request, 'apps/teacher-dashboard.html', context)