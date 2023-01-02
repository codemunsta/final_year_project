from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from users.models import Portal, Student
from django.contrib import messages
from .models import Hall, Block, Floor, RoomA, RoomB, RoomC, SpaceUp, SpaceDown
from . import space_calculator


def all_view(request):  # url set
    halls = Hall.objects.all()

    context = {
        'halls': halls
    }
    return render(request, 'home.html', context)


def explore_hostel(request, hall_name):
    hall = Hall.objects.get(hall_name=hall_name)

    free = hall.free_space
    total = hall.number_of_spaces
    available_space = int((free/100) * total)
    unavailable = total-available_space

    context = {
        'hall': hall,
        'available': available_space,
        'unavailable': unavailable,
    }
    return render(request, 'hall.html', context)


def book_view(request):  # url set

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        halls = []
        if student.sex == 'Male':
            hall_3 = Hall.objects.get(hall_name='Hall_3')
            hall_4 = Hall.objects.get(hall_name='Hall_4')
            hall_5 = Hall.objects.get(hall_name='Hall_5')

            halls.append(hall_3)
            halls.append(hall_4)
            halls.append(hall_5)

            context = {
                'halls': halls
            }
            return render(request, 'book_hall.html', context)
        elif student.sex == 'Female':
            hall_1 = Hall.objects.get(hall_name='Hall_1')
            hall_2 = Hall.objects.get(hall_name='Hall_2')
            hall_3 = Hall.objects.get(hall_name='Hall_3')
            hall_5 = Hall.objects.get(hall_name='Hall_5')

            halls.append(hall_1)
            halls.append(hall_2)
            halls.append(hall_3)
            halls.append(hall_5)

            context = {
                'halls': halls
            }

            return render(request, 'book_hall.html', context)
    else:
        messages.info(request, 'Login to view or book hostels')
        return redirect('login')


def block_view(request, hall):  # url set

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        hall = Hall.objects.get(hall_name=hall)
        blocks = Block.objects.filter(hostel=hall, sex=student.sex)
        block_all = []
        for block in blocks:
            floors = Floor.objects.filter(block=block)
            name = block.block_name
            blk = {
                'block': block,
                'floors': floors
            }
            block_all.append(blk)

        context = {
            'blocks': block_all
        }
        return render(request, 'block.html', context)
    else:
        messages.info('Login to view or book hostels')
        return redirect('login')


def floor_rooms(request, slug):  # url set

    if request.user.is_authenticated:
        floor = Floor.objects.get(slug=slug)
        hall = Hall.objects.get(id=floor.block.hostel.id)
        match hall.hall_name:
            case 'Hall_1':
                rooms = RoomB.objects.filter(floor=floor)
                context = {
                    'rooms': rooms
                }
                return render(request, 'floor_rooms.html', context)
            case 'Hall_2' | 'Hall_3' | 'Hall_4':
                rooms = RoomA.objects.filter(floor=floor)
                context = {
                    'rooms': rooms
                }
                return render(request, 'floor_rooms.html', context)
            case 'Hall_5':
                rooms = RoomC.objects.filter(floor=floor)
                context = {
                    'rooms': rooms
                }
                return render(request, 'floor_rooms.html', context)
            case _:
                messages.info('Opps, Whoa what happened there, lets try again')
                return redirect('hostel')
    else:
        messages.info('Login to view or book hostels')
        return redirect('login')


def room_view(request, slug):  # url set

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        context = {}
        if student.booking:
            match student.space:
                case 'UP':
                    space = SpaceUp.objects.filter(student=student)
                    if space.reserved:
                        messages.info('your space has been reserved for you, you can"t book again')
                        context['book'] = False
                    else:
                        messages.info(
                            'Warning you have booked a space, booking again would cancel any previous booking')
                case 'DOWN':
                    space = SpaceDown.objects.filter(student=student)
                    if space.reserved:
                        messages.info('your space has been reserved for you, you can"t book again')
                        context['book'] = False
                    else:
                        messages.info(
                            'Warning you have booked a space, booking again would cancel any previous booking')
                case _:
                    pass
        if 'Hall_1' in slug:
            room = RoomB.objects.get(slug=slug)
            context['room'] = room
            return render(request, 'room_b.html', context)
        elif 'Hall_2' or 'Hall_3' or 'Hall_4' or 'Hall_5' in slug:
            room = RoomA.objects.get(slug=slug)
            context['room'] = room
            return render(request, 'room_A.html', context)
    else:
        messages.info('Login to view or book hostels')
        return redirect('login')


def book_space(request, pos, pk):  # url set

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        match pos:
            case 'up':
                space = SpaceUp.objects.get(id=pk)
                if space.Free:
                    space.student = student
                    space.Free = False
                    space.Booked = True
                    space.save()

                    student.booking = True
                    student.space = 'UP'
                    student.save()

                    match space.room_type:
                        case 'roomA':
                            room = RoomA.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomA')
                        case 'roomB':
                            room = RoomB.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomB')
                        case 'roomC':
                            room = RoomC.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomC')
                        case _:
                            pass
                    return redirect('dashboard', pk=student.id)
                else:
                    messages.info('You cannot book and already booked space')
                    return redirect('dashboard', pk=student.id)
            case 'down':
                space = SpaceDown.objects.get(id=pk)
                if space.Free:
                    space.student = student
                    space.Free = False
                    space.Booked = True
                    space.save()

                    student.booking = True
                    student.space = 'DOWN'
                    student.save()

                    match space.room_type:
                        case 'roomA':
                            room = RoomA.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomA')
                        case 'roomB':
                            room = RoomB.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomB')
                        case 'roomC':
                            room = RoomC.objects.get(id=space.room_id)
                            space_calculator.space_booked(room_id=room.id, room_type='roomC')
                        case _:
                            pass
                    return redirect('dashboard', pk=student.id)
                else:
                    messages.info('You cannot book and already booked space')
                    return redirect('dashboard', pk=student.id)
            case _:
                messages.info('invalid request')
                return redirect('hostel')
    else:
        messages.info('Login to view or book hostels')
        return redirect('login')


def un_book(request, pos, pk):

    if request.user.is_authenticated:
        student = Student.objects.get(stud=request.user)
        match pos:
            case 'UP':
                try:
                    space = SpaceUp.objects.get(id=pk, student=student)
                    space.Booked = False
                    space.Free = True
                    space.student = None
                    space.save()

                    student.booking = False
                    student.space = ''
                    student.save()

                    match space.room_type:
                        case 'roomA':
                            room = RoomA.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomA')
                            return redirect('dashboard', pk=student.id)
                        case 'roomB':
                            room = RoomB.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomB')
                            return redirect('dashboard', pk=student.id)
                        case 'roomC':
                            room = RoomC.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomC')
                            return redirect('dashboard', pk=student.id)
                        case _:
                            return redirect('dashboard', pk=student.id)
                except ObjectDoesNotExist:
                    messages.info(request, "You can't cancel a booking that wasn't done by you")
                    print("You can't cancel a booking that wasn't done by you")
                    return redirect('hostel')
            case 'DOWN':
                try:
                    space = SpaceDown.objects.get(id=pk, student=student)
                    space.Booked = False
                    space.Free = True
                    space.student = None
                    space.save()

                    student.booking = False
                    student.space = ''
                    student.save()

                    match space.room_type:
                        case 'roomA':
                            room = RoomA.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomA')
                            return redirect('dashboard', pk=student.id)
                        case 'roomB':
                            room = RoomB.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomB')
                            return redirect('dashboard', pk=student.id)
                        case 'roomC':
                            room = RoomC.objects.get(id=space.room_id)
                            space_calculator.space_unbooked(room_id=room.id, room_type='roomC')
                            return redirect('dashboard', pk=student.id)
                        case _:
                            return redirect('dashboard', pk=student.id)
                except ObjectDoesNotExist:
                    messages.info(request, "You can't cancel a booking that wasn't done by you")
                    return redirect('hostel')
            case _:
                messages.info(request, 'invalid request')
                return redirect('hostel')
    else:
        messages.info(request, 'Login to view or book hostels')
        return redirect('login')


def index(request):
    student = Student.objects.get(stud=request.user)
    context = {
        'student': student,
    }
    if SpaceUp.objects.get(student=student).exist():
        space = SpaceUp.objects.get(student=student)
        context['space'] = space
    elif SpaceDown.objects.get(student=student).exist():
        space = SpaceDown.objects.get(student=student)
        context['space'] = space
    else:
        print('no space booked yet')
    return render(request, 'halls.html', context)


def view_hostel(request):
    student = Student.objects.get(stud=request.user)
    context = {
        'student': student,
    }
    if SpaceUp.objects.get(student=student).exist():
        space = SpaceUp.objects.get(student=student)
        try:
            room = space.roomA
            roommates_up = SpaceUp.objects.filter(roomA=room)
            roommates_down = SpaceDown.objects.filter(roomA=room)
            context['roommates_up'] = roommates_up
            context['roommates_down'] = roommates_down
            context['space'] = space
            context['room'] = room
            context['floor'] = room.floor
            context['block'] = room.floor.block
            context['hall'] = room.floor.block.hostel
        except ObjectDoesNotExist:
            try:
                room = space.roomB
                roommates_up = SpaceUp.objects.filter(roomB=room)
                roommates_down = SpaceDown.objects.filter(roomB=room)
                context['roommates_up'] = roommates_up
                context['roommates_down'] = roommates_down
                context['space'] = space
                context['room'] = room
                context['floor'] = room.floor
                context['block'] = room.floor.block
                context['hall'] = room.floor.block.hostel
            except ObjectDoesNotExist:
                try:
                    room = space.roomC
                    roommates_up = SpaceUp.objects.filter(roomC=room)
                    roommates_down = SpaceDown.objects.filter(roomC=room)
                    context['roommates_up'] = roommates_up
                    context['roommates_down'] = roommates_down
                    context['space'] = space
                    context['room'] = room
                    context['floor'] = room.floor
                    context['block'] = room.floor.block
                    context['hall'] = room.floor.block.hostel
                except ObjectDoesNotExist:
                    pass
    elif SpaceDown.objects.get(student=student).exist():
        space = SpaceDown.objects.get(student=student)
        try:
            room = space.roomA
            roommates_up = SpaceUp.objects.filter(roomA=room)
            roommates_down = SpaceDown.objects.filter(roomA=room)
            context['roommates_up'] = roommates_up
            context['roommates_down'] = roommates_down
            context['space'] = space
            context['room'] = room
            context['floor'] = room.floor
            context['block'] = room.floor.block
            context['hall'] = room.floor.block.hostel
        except ObjectDoesNotExist:
            try:
                room = space.roomB
                roommates_up = SpaceUp.objects.filter(roomB=room)
                roommates_down = SpaceDown.objects.filter(roomB=room)
                context['roommates_up'] = roommates_up
                context['roommates_down'] = roommates_down
                context['space'] = space
                context['room'] = room
                context['floor'] = room.floor
                context['block'] = room.floor.block
                context['hall'] = room.floor.block.hostel
            except ObjectDoesNotExist:
                try:
                    room = space.roomC
                    roommates_up = SpaceUp.objects.filter(roomC=room)
                    roommates_down = SpaceDown.objects.filter(roomC=room)
                    context['roommates_up'] = roommates_up
                    context['roommates_down'] = roommates_down
                    context['space'] = space
                    context['room'] = room
                    context['floor'] = room.floor
                    context['block'] = room.floor.block
                    context['hall'] = room.floor.block.hostel
                except ObjectDoesNotExist:
                    pass
    return render(request, 'hostel_view.html', context)