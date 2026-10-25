from django.db import migrations

# Areas inside Dhaka only
LOCATIONS = [
    'Agargaon', 'Badda', 'Banani', 'Baridhara', 'Bashundhara R/A',
    'Cantonment', 'Demra', 'Dhanmondi', 'Farmgate', 'Gulistan',
    'Gulshan', 'Jatrabari', 'Kafrul', 'Kalabagan', 'Kallyanpur',
    'Khilgaon', 'Lalbagh', 'Malibagh', 'Mirpur', 'Moghbazar',
    'Mohammadpur', 'Motijheel', 'Nikunja', 'Old Dhaka', 'Pallabi',
    'Rampura', 'Shahbagh', 'Shantinagar', 'Shyamoli', 'Tejgaon',
    'Uttara', 'Wari',
]

# (name, font-awesome icon, description, optional picture for the home page)
SERVICES = [
    ('AC Repair', 'snowflake', 'AC servicing, gas refill and repair.',
     'https://images.unsplash.com/photo-1631545806161-5121b66b26d3?auto=format&fit=crop&w=500&q=80'),
    ('Appliance Repair', 'screwdriver-wrench', 'Fridge, washing machine, oven and other home appliances.', ''),
    ('Carpentry', 'hammer', 'Furniture repair, doors, windows and woodwork.', ''),
    ('Chef', 'utensils', 'Home cooks and chefs for daily meals or events.', ''),
    ('Driver', 'car', 'Experienced drivers for daily or one-time trips.', ''),
    ('Electrical', 'bolt', 'Wiring, switches, lights, fans and electrical faults.',
     'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=500&q=80'),
    ('Gardener', 'seedling', 'Garden and rooftop plant care.', ''),
    ('Home Cleaning', 'broom', 'Deep cleaning for flats, houses and offices.',
     'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=500&q=80'),
    ('Laundry', 'shirt', 'Washing, ironing and dry cleaning.', ''),
    ('Painting', 'paint-roller', 'Interior and exterior wall painting.',
     'https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=500&q=80'),
    ('Pest Control', 'bug', 'Cockroach, termite, mosquito and rodent control.', ''),
    ('Plumbing', 'faucet', 'Leaks, taps, pipes, tanks and bathroom fittings.',
     'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=500&q=80'),
]


def add_data(apps, schema_editor):
    Location = apps.get_model('acc', 'Location')
    Service = apps.get_model('acc', 'Service')

    for name in LOCATIONS:
        Location.objects.get_or_create(name=name)

    for name, icon, description, image_url in SERVICES:
        Service.objects.get_or_create(
            name=name,
            defaults={'icon': icon, 'description': description, 'image_url': image_url},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_data, migrations.RunPython.noop),
    ]
from django.db import migrations

# Areas inside Dhaka only
LOCATIONS = [
    'Agargaon', 'Badda', 'Banani', 'Baridhara', 'Bashundhara R/A',
    'Cantonment', 'Demra', 'Dhanmondi', 'Farmgate', 'Gulistan',
    'Gulshan', 'Jatrabari', 'Kafrul', 'Kalabagan', 'Kallyanpur',
    'Khilgaon', 'Lalbagh', 'Malibagh', 'Mirpur', 'Moghbazar',
    'Mohammadpur', 'Motijheel', 'Nikunja', 'Old Dhaka', 'Pallabi',
    'Rampura', 'Shahbagh', 'Shantinagar', 'Shyamoli', 'Tejgaon',
    'Uttara', 'Wari',
]

# (name, font-awesome icon, description, optional picture for the home page)
SERVICES = [
    ('AC Repair', 'snowflake', 'AC servicing, gas refill and repair.',
     'https://images.unsplash.com/photo-1631545806161-5121b66b26d3?auto=format&fit=crop&w=500&q=80'),
    ('Appliance Repair', 'screwdriver-wrench', 'Fridge, washing machine, oven and other home appliances.', ''),
    ('Carpentry', 'hammer', 'Furniture repair, doors, windows and woodwork.', ''),
    ('Chef', 'utensils', 'Home cooks and chefs for daily meals or events.', ''),
    ('Driver', 'car', 'Experienced drivers for daily or one-time trips.', ''),
    ('Electrical', 'bolt', 'Wiring, switches, lights, fans and electrical faults.',
     'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=500&q=80'),
    ('Gardener', 'seedling', 'Garden and rooftop plant care.', ''),
    ('Home Cleaning', 'broom', 'Deep cleaning for flats, houses and offices.',
     'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=500&q=80'),
    ('Laundry', 'shirt', 'Washing, ironing and dry cleaning.', ''),
    ('Painting', 'paint-roller', 'Interior and exterior wall painting.',
     'https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=500&q=80'),
    ('Pest Control', 'bug', 'Cockroach, termite, mosquito and rodent control.', ''),
    ('Plumbing', 'faucet', 'Leaks, taps, pipes, tanks and bathroom fittings.',
     'https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=500&q=80'),
]


def add_data(apps, schema_editor):
    Location = apps.get_model('acc', 'Location')
    Service = apps.get_model('acc', 'Service')

    for name in LOCATIONS:
        Location.objects.get_or_create(name=name)

    for name, icon, description, image_url in SERVICES:
        Service.objects.get_or_create(
            name=name,
            defaults={'icon': icon, 'description': description, 'image_url': image_url},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_data, migrations.RunPython.noop),
    ]
