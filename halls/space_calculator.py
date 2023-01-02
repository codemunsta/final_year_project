from .models import RoomA, RoomB, RoomC, Floor, Block


def space_booked(room_id, room_type):

    match room_type:
        case 'roomA':
            room = RoomA.objects.get(id=room_id)
            room.free_space = room.free_space - 12.5
            room .save()

            floor = Floor.objects.get(id=room.floor.id)
            block = Block.objects.get(id=floor.block.id)
            if block.hostel.hall_name == 'Hall_4':
                floor.free_space = floor.free_space - 0.0052
                floor.save()
                block.free_space = block.free_space - 0.0052
                block.save()
                hostel = block.hostel
                hostel.free_space = hostel.free_space - 0.0013
                hostel.save()
                return
            else:
                floor.free_space = floor.free_space - 1.5625
                floor.save()
                block.free_space = block.free_space - 0.390
                block.save()
                hostel = block.hostel
                hostel.free_space = hostel.free_space - 0.0558
                hostel.save()
                return
        case 'roomB':
            room = RoomB.objects.get(id=room_id)
            room.free_space = room.free_space - 16.6
            room.save()
            floor = Floor.objects.get(id=room.floor.id)
            floor.free_space = floor.free_space - 2.083
            floor.save()
            block = Block.objects.get(id=floor.block.id)
            block.free_space = block.free_space - 0.694
            block.save()
            hostel = block.hostel
            hostel.free_space = hostel.free_space - 0.1157
            hostel.save()
            return
        case 'roomC':
            room = RoomC.objects.get(id=room_id)
            room.free_space = room.free_space - 25
            room.save()
            floor = Floor.objects.get(id=room.floor.id)
            floor.free_space = floor.free_space - 3.125
            floor.save()
            block = Block.objects.get(id=floor.block.id)
            block.free_space = block.free_space - 1.563
            block.save()
            hostel = block.hostel
            hostel.free_space = hostel.free_space - 0.781
            hostel.save()
            return
        case _:
            return 0


def space_unbooked(room_id, room_type):

    match room_type:
        case 'roomA':
            room = RoomA.objects.get(id=room_id)
            room.free_space = room.free_space + 12.5
            room .save()

            floor = Floor.objects.get(id=room.floor.id)
            block = Block.objects.get(id=floor.block.id)
            if block.hostel.hall_name == 'hall_4':
                floor.free_space = floor.free_space + 0.0052
                floor.save()
                block.free_space = block.free_space + 0.0052
                block.save()
                hostel = block.hostel
                hostel.free_space = hostel.free_space + 0.0013
                hostel.save()
                return
            else:
                floor.free_space = floor.free_space + 1.5625
                floor.save()
                block.free_space = block.free_space + 0.390
                block.save()
                hostel = block.hostel
                hostel.free_space = hostel.free_space + 0.0558
                hostel.save()
                return
        case 'roomB':
            room = RoomB.objects.get(id=room_id)
            room.free_space = room.free_space + 16.6
            room.save()
            floor = Floor.objects.get(id=room.floor.id)
            floor.free_space = floor.free_space + 2.083
            floor.save()
            block = Block.objects.get(id=floor.block.id)
            block.free_space = block.free_space + 0.694
            block.save()
            hostel = block.hostel
            hostel.free_space = hostel.free_space + 0.1157
            hostel.save()
            return
        case 'roomC':
            room = RoomC.objects.get(id=room_id)
            room.free_space = room.free_space + 25
            room.save()
            floor = Floor.objects.get(id=room.floor.id)
            floor.free_space = floor.free_space + 3.125
            floor.save()
            block = Block.objects.get(id=floor.block.id)
            block.free_space = block.free_space + 1.563
            block.save()
            hostel = block.hostel
            hostel.free_space = hostel.free_space + 0.781
            hostel.save()
            return
        case _:
            return 0



