import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(default='screwdriver-wrench', max_length=50)),
                ('image_url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Serviceman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid mobile number like 01712345678.', regex='^(\\+?88)?01[3-9]\\d{8}$')])),
                ('address', models.CharField(max_length=255)),
                ('experience', models.PositiveIntegerField(default=0)),
                ('bio', models.TextField(blank=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicemen', to='acc.location')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicemen', to='acc.service')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid mobile number like 01712345678.', regex='^(\\+?88)?01[3-9]\\d{8}$')])),
                ('address', models.CharField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customers', to='acc.location')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('booking_date', models.DateField()),
                ('booking_time', models.TimeField()),
                ('offered_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('serviceman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='acc.serviceman')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='acc.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
