from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Portal, Student
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist


class Hall(models.Model):

    HALL_NAME = (
        ('Hall_1', 'Hall_1'),
        ('Hall_2', 'Hall_2'),
        ('Hall_3', 'Hall_3'),
        ('Hall_4', 'Hall_4'),
        ('Hall_5', 'Hall_5'),
    )
    admin_head = models.ForeignKey(Portal, null=True, blank=True, on_delete=models.SET_NULL, related_name='admin_head')
    portal_one = models.ForeignKey(Portal, null=True, blank=True, on_delete=models.SET_NULL, related_name='portal_one')
    portal_two = models.ForeignKey(Portal, null=True, blank=True, on_delete=models.SET_NULL, related_name='portal_two')
    hall_name = models.CharField(max_length=30, choices=HALL_NAME, unique=True)
    name = models.CharField(max_length=50, null=True)
    number_of_rooms = models.IntegerField(null=True)
    number_of_spaces = models.IntegerField(null=True)
    back_img = models.ImageField(blank=True, null=True, upload_to=f'hall/images')
    img_one = models.ImageField(blank=True, null=True, upload_to=f'hall/images')
    img_two = models.ImageField(blank=True, null=True, upload_to=f'hall/images')
    img_three = models.ImageField(blank=True, null=True, upload_to=f'hall/images')
    descriptions = models.TextField(null=True)
    free_space = models.FloatField(default=100.00)

    def __str__(self):
        return self.hall_name

    def get_absolute_url(self):
        return reverse('hostel', kwargs={'hall_name': self.hall_name})


@receiver(post_save, sender=Hall)
def setup_blocks(sender, instance=None, created=False, **kwargs):

    if created:
        match instance.hall_name:
            case 'Hall_1':
                block_a = Block.objects.create(hostel=instance, block_name='Block_A', number_of_floors=3, sex='Female')
                block_a.save()
                block_b = Block.objects.create(hostel=instance, block_name='Block_B', number_of_floors=3, sex='Female')
                block_b.save()
                block_c = Block.objects.create(hostel=instance, block_name='Block_C', number_of_floors=3, sex='Female')
                block_c.save()
                block_d = Block.objects.create(hostel=instance, block_name='Block_D', number_of_floors=3, sex='Female')
                block_d.save()
                block_e = Block.objects.create(hostel=instance, block_name='Block_E', number_of_floors=3, sex='Female')
                block_e.save()
                block_f = Block.objects.create(hostel=instance, block_name='Block_F', number_of_floors=3, sex='Female')
                block_f.save()
            case 'Hall_2':
                block_a = Block.objects.create(hostel=instance, block_name='Block_A', number_of_floors=4, sex='Female')
                block_a.save()
                block_b = Block.objects.create(hostel=instance, block_name='Block_B', number_of_floors=4, sex='Female')
                block_b.save()
                block_c = Block.objects.create(hostel=instance, block_name='Block_C', number_of_floors=4, sex='Female')
                block_c.save()
                block_d = Block.objects.create(hostel=instance, block_name='Block_D', number_of_floors=4, sex='Female')
                block_d.save()
                block_e = Block.objects.create(hostel=instance, block_name='Block_E', number_of_floors=4, sex='Female')
                block_e.save()
                block_f = Block.objects.create(hostel=instance, block_name='Block_F', number_of_floors=4, sex='Female')
                block_f.save()
                block_g = Block.objects.create(hostel=instance, block_name='Block_G', number_of_floors=4, sex='Female')
                block_g.save()
            case 'Hall_3':
                block_a = Block.objects.create(hostel=instance, block_name='Block_A', number_of_floors=4, sex='Male')
                block_a.save()
                block_b = Block.objects.create(hostel=instance, block_name='Block_B', number_of_floors=4, sex='Male')
                block_b.save()
                block_c = Block.objects.create(hostel=instance, block_name='Block_C', number_of_floors=4, sex='Male')
                block_c.save()
                block_d = Block.objects.create(hostel=instance, block_name='Block_D', number_of_floors=4, sex='Female')
                block_d.save()
                block_e = Block.objects.create(hostel=instance, block_name='Block_E', number_of_floors=4, sex='Female')
                block_e.save()
                block_f = Block.objects.create(hostel=instance, block_name='Block_F', number_of_floors=4, sex='Female')
                block_f.save()
                block_g = Block.objects.create(hostel=instance, block_name='Block_G', number_of_floors=4, sex='Female')
                block_g.save()
            case 'Hall_4':
                block_a = Block.objects.create(hostel=instance, block_name='Block_A', number_of_floors=1, sex='Male')
                block_a.save()
                block_b = Block.objects.create(hostel=instance, block_name='Block_B', number_of_floors=1, sex='Male')
                block_b.save()
                block_c = Block.objects.create(hostel=instance, block_name='Block_C', number_of_floors=1, sex='Male')
                block_c.save()
                block_d = Block.objects.create(hostel=instance, block_name='Block_D', number_of_floors=1, sex='Female')
                block_d.save()
            case 'Hall_5':
                block_a = Block.objects.create(hostel=instance, block_name='Block_A', number_of_floors=2, sex='Male')
                block_a.save()
                block_b = Block.objects.create(hostel=instance, block_name='Block_B', number_of_floors=2, sex='Female')
                block_b.save()
            case _:
                pass


class SpaceUp(models.Model):

    ROOM_TYPE = (
        ('roomA', 'roomA'),
        ('roomB', 'roomB'),
    )
    student = models.OneToOneField(Student, null=True, blank=True, on_delete=models.SET_NULL)
    Free = models.BooleanField(default=True)
    Booked = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)
    room_type = models.CharField(max_length=6, choices=ROOM_TYPE, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)


class SpaceDown(models.Model):
    ROOM_TYPE = (
        ('roomA', 'roomA'),
        ('roomB', 'roomB'),
    )
    student = models.OneToOneField(Student, null=True, blank=True, on_delete=models.SET_NULL)
    Free = models.BooleanField(default=True)
    Booked = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)
    room_type = models.CharField(max_length=6, choices=ROOM_TYPE, null=True, blank=True)
    room_id = models.IntegerField(null=True, blank=True)


class Block(models.Model):

    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    hostel = models.ForeignKey(Hall, on_delete=models.CASCADE)
    block_name = models.CharField(max_length=10)
    number_of_floors = models.IntegerField()
    sex = models.CharField(choices=SEX, max_length=6)
    free_space = models.FloatField(default=100.00)

    def __str__(self):
        return f'{self.block_name} | {self.hostel.hall_name}'


@receiver(post_save, sender=Block)
def setup_floors(sender, instance=None, created=False, **kwargs):

    if created:
        match instance.hostel.hall_name:
            case 'Hall_1':
                for floors in range(instance.number_of_floors):
                    floor = Floor.objects.create(block=instance, floor_number=int(floors), number_of_rooms=8)
                    floor.save()
            case 'Hall_2':
                for floors in range(instance.number_of_floors):
                    floor = Floor.objects.create(block=instance, floor_number=int(floors), number_of_rooms=8)
                    floor.save()
            case 'Hall_3':
                for floors in range(instance.number_of_floors):
                    floor = Floor.objects.create(block=instance, floor_number=int(floors), number_of_rooms=8)
                    floor.save()
            case 'Hall_4':
                for floors in range(instance.number_of_floors):
                    floor = Floor.objects.create(block=instance, floor_number=int(floors), number_of_rooms=24)
                    floor.save()
            case 'Hall_5':
                for floors in range(instance.number_of_floors):
                    floor = Floor.objects.create(block=instance, floor_number=int(floors), number_of_rooms=8)
                    floor.save()
            case _:
                pass


class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    number_of_rooms = models.IntegerField()
    free_space = models.FloatField(default=100.00)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.floor_number} | {self.block.block_name} | {self.block.hostel.hall_name}'


@receiver(post_save, sender=Floor)
def setup_rooms(sender, instance=None, created=False, **kwargs):

    if created:
        instance.slug = f'{instance.floor_number}_{instance.block.block_name}_{instance.block.hostel.hall_name}'
        match instance.block.hostel.hall_name:
            case 'Hall_1':
                for room in range(instance.number_of_rooms):
                    r = RoomB.objects.create(floor=instance, room_number=int(room))
                    r.save()
            case 'Hall_2':
                for room in range(instance.number_of_rooms):
                    r = RoomA.objects.create(floor=instance, room_number=int(room))
                    r.save()
            case 'Hall_3':
                for room in range(instance.number_of_rooms):
                    r = RoomA.objects.create(floor=instance, room_number=int(room))
                    r.save()
            case 'Hall_4':
                for room in range(instance.number_of_rooms):
                    r = RoomA.objects.create(floor=instance, room_number=int(room))
                    r.save()
            case 'Hall_5':
                for room in range(instance.number_of_rooms):
                    r = RoomA.objects.create(floor=instance, room_number=int(room))
                    r.save()
            case _:
                pass

        instance.save()


class RoomA(models.Model):
    room_number = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    space_1 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='Aspace1')
    space_2 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='Aspace2')
    space_3 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='Aspace3')
    space_4 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='Aspace4')
    space_5 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='Aspace5')
    space_6 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='Aspace6')
    space_7 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='Aspace7')
    space_8 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='Aspace8')
    resource_in_use = models.BooleanField(default=False)
    free_space = models.FloatField(default=100.00)
    slug = models.SlugField()

    def __str__(self):
        return f'Room {self.room_number} | Floor {self.floor.floor_number} | {self.floor.block.block_name} | ' \
               f'{self.floor.block.hostel.hall_name}'


@receiver(post_save, sender=RoomA)
def setup_spaces(sender, instance=None, created=False, **kwargs):

    if created:
        instance.slug = f'{instance.room_number}_{instance.floor.slug}'
        instance.space_1 = SpaceUp.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_2 = SpaceDown.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_3 = SpaceUp.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_4 = SpaceDown.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_5 = SpaceUp.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_6 = SpaceDown.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_7 = SpaceUp.objects.create(room_type='roomA', room_id=instance.id)
        instance.space_8 = SpaceDown.objects.create(room_type='roomA', room_id=instance.id)

        instance.save()


class RoomB(models.Model):
    room_number = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    space_1 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='B_space1')
    space_2 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='B_space2')
    space_3 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='B_space3')
    space_4 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='B_space4')
    space_5 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='B_space5')
    space_6 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='B_space6')
    resource_in_use = models.BooleanField(default=False)
    free_space = models.FloatField(default=100.00)

    def __str__(self):
        return f'Room {self.room_number} | Floor {self.floor.floor_number} | {self.floor.block.block_name} | ' \
               f'{self.floor.block.hostel.hall_name}'


@receiver(post_save, sender=RoomB)
def setup_spaces(sender, instance=None, created=False, **kwargs):

    if created:
        instance.slug = f'{instance.room_number}_{instance.floor.slug}'
        instance.space_1 = SpaceUp.objects.create(room_type='roomB', room_id=instance.id)
        instance.space_2 = SpaceDown.objects.create(room_type='roomB', room_id=instance.id)
        instance.space_3 = SpaceUp.objects.create(room_type='roomB', room_id=instance.id)
        instance.space_4 = SpaceDown.objects.create(room_type='roomB', room_id=instance.id)
        instance.space_5 = SpaceUp.objects.create(room_type='roomB', room_id=instance.id)
        instance.space_6 = SpaceDown.objects.create(room_type='roomB', room_id=instance.id)

        instance.save()


class RoomC(models.Model):
    room_number = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    space_1 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='C_space1')
    space_2 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='C_space2')
    space_3 = models.OneToOneField(SpaceUp, null=True, on_delete=models.SET_NULL, related_name='C_space3')
    space_4 = models.OneToOneField(SpaceDown, null=True, on_delete=models.SET_NULL, related_name='C_space4')
    resource_in_use = models.BooleanField(default=False)
    free_space = models.FloatField(default=100.00)

    def __str__(self):
        return f'Room {self.room_number} | Floor {self.floor.floor_number} | {self.floor.block.block_name} | ' \
               f'{self.floor.block.hostel.hall_name}'


@receiver(post_save, sender=RoomC)
def setup_spaces(sender, instance=None, created=False, **kwargs):

    if created:
        instance.slug = f'{instance.room_number}_{instance.floor.slug}'
        instance.space_1 = SpaceUp.objects.create(room_type='roomC', room_id=instance.id)
        instance.space_2 = SpaceDown.objects.create(room_type='roomC', room_id=instance.id)
        instance.space_3 = SpaceUp.objects.create(room_type='roomC', room_id=instance.id)
        instance.space_4 = SpaceDown.objects.create(room_type='roomC', room_id=instance.id)

        instance.save()
# Create your models here.
