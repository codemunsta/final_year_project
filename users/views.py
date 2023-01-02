from .models import Student
from django.contrib import messages
from halls import models as hall_models
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from .documents_check import school_fees_check, bed_allocation_check


def register_view(request):  # Done
    context = {}

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)

    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['mat_number'])
            messages.info(request, 'MatNo already exist, please log in')
            return redirect('login.html')
        except ObjectDoesNotExist:
            username = request.POST['mat_number']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            mat_number = request.POST['mat_number']
            department = request.POST['department']
            sex = request.POST['sex']
            level = request.POST['level']
            school_fees = request.FILES['school_fees']
            hostel_application = request.FILES['hostel_application']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                filestorage = FileSystemStorage()
                school_fees_pdf = filestorage.save(school_fees.name, school_fees)
                check_1 = school_fees_check(filestorage.path(school_fees_pdf), mat_no=mat_number, session='2020/2021')
                if check_1 == 0:
                    filestorage2 = FileSystemStorage()
                    hostel_application_pdf = filestorage2.save(hostel_application.name, hostel_application)
                    check_2 = bed_allocation_check(filestorage2.path(hostel_application_pdf), mat_no=mat_number, session='2019/2020')
                    if check_2 == 0:
                        user = User.objects.create_user(username=username, email=email, password=password)
                        user.first_name = firstname
                        user.last_name = lastname
                        user.save()
                        student = Student.objects.create(
                            stud=user,
                            mat_no=mat_number,
                            department=department,
                            level=level,
                            sex=sex,
                            school_fees=school_fees_pdf,
                            hostel_application=hostel_application_pdf,
                            slug=user.username
                        )
                        student.save()
                        user = authenticate(request, username=username, password=password)
                        login(request, user)
                        messages.info(request, "Verification Successful")
                        student = Student.objects.get(stud=request.user)
                        return redirect('dashboard', pk=student.id)
                    else:
                        messages.error(request, f'{check_2}')
                        return render(request, 'registration/register.html', context)
                else:
                    messages.error(request, f'{check_1}')
                    return render(request, 'registration/register.html', context)
            else:
                messages.error(request, 'Password does not match')
                return render(request, 'registration/register.html', context)
    else:
        return render(request, 'registration/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        return redirect('dashboard', pk=student.id)
    if request.method == 'POST':
        username = request.POST['mat_number']
        password = request.POST["password"]
        check_user = User.objects.filter(username=username).exists()
        if check_user is False:
            messages.info(request, "MatNo not registered")
            print('no')
            return redirect('login')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, "Successfully logged in.")
            student = Student.objects.get(stud=user)
            return redirect('dashboard', pk=student.id)
        else:
            messages.info(request, 'invalid login details')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    return redirect('index')


class Dashboard(DetailView):

    model = Student
    template_name = 'registration/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        student = Student.objects.get(stud=self.request.user)
        if student.booking:
            if student.space == 'UP':
                space = hall_models.SpaceUp.objects.get(student=student)
                space_type = 'up'

                match space.room_type:
                    case 'roomA':
                        try:
                            room = hall_models.RoomA.objects.get(space_1=space)
                        except ObjectDoesNotExist:
                            try:
                                room = hall_models.RoomA.objects.get(space_3=space)
                            except ObjectDoesNotExist:
                                try:
                                    room = hall_models.RoomA.objects.get(space_5=space)
                                except ObjectDoesNotExist:
                                    room = hall_models.RoomA.objects.get(space_7=space)

                        spaces = []
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace1=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace3=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace5=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace7=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace4=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace6=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace8=room))
                    case 'roomB':
                        try:
                            room = hall_models.RoomB.objects.get(space_1=space)
                        except ObjectDoesNotExist:
                            try:
                                room = hall_models.RoomB.objects.get(space_3=space)
                            except ObjectDoesNotExist:
                                room = hall_models.RoomB.objects.get(space_5=space)
                        spaces = []
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace1=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace3=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace5=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                    case _:
                        return context
            elif student.space == 'DOWN':
                space = hall_models.SpaceDown.objects.get(student=student)
                space_type = 'down'

                match space.room_type:
                    case 'roomA':
                        try:
                            room = hall_models.RoomA.objects.get(space_2=space)
                        except ObjectDoesNotExist:
                            try:
                                room = hall_models.RoomA.objects.get(space_4=space)
                            except ObjectDoesNotExist:
                                try:
                                    room = hall_models.RoomA.objects.get(space_6=space)
                                except ObjectDoesNotExist:
                                    room = hall_models.RoomA.objects.get(space_8=space)

                        spaces = []
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace1=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace3=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace5=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Aspace7=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace4=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace6=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Aspace8=room))
                    case 'roomB':
                        try:
                            room = hall_models.RoomB.objects.get(space_2=space)
                        except ObjectDoesNotExist:
                            try:
                                room = hall_models.RoomB.objects.get(space_4=space)
                            except ObjectDoesNotExist:
                                room = hall_models.RoomB.objects.get(space_6=space)

                        spaces = []
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace1=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace3=room))
                        spaces.append(hall_models.SpaceUp.objects.get(Bspace5=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                        spaces.append(hall_models.SpaceDown.objects.get(Bspace2=room))
                    case _:
                        return context
            else:
                messages.info('Error retreiving space booked, Please re book hostel')
                student.booking = False
                student.save()
                return context

            floor = room.floor
            block = floor.block
            hall = block.hostel

            context['hall'] = hall
            context['block'] = block
            context['floor'] = floor
            context['room'] = room
            context['space'] = space_type
            context['spaces'] = spaces
            context['i_space'] = space

        return context


def display_room(request, pk):
    space = hall_models.SpaceUp.objects.get(id=pk)
    room = hall_models.RoomA.objects.get(space_7=space)
    spaces = hall_models.SpaceUp.objects.get(Aspace1=room)
    context = {
        'space': space,
        'room': room,
        'spaces': spaces
    }
    return render(request, 'space.html', context)
    pass


# Create your views here.
