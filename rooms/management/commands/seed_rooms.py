import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This Command creates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(10, 1000),
                "beds": lambda x: random.randint(0, 5),
                "guests": lambda x: random.randint(1, 10),
                "bedrooms": lambda x: random.randint(0, 5),
                "baths": lambda x: random.randint(0, 5),
            },
        )
        created_room_pk = seeder.execute()
        created_clean = flatten(list(created_room_pk.values()))
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 19)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(1, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} Rooms created!"))
