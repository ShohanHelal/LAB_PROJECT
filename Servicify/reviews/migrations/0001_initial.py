import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(5, '5 - Excellent'), (4, '4 - Good'), (3, '3 - Okay'), (2, '2 - Poor'), (1, '1 - Terrible')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='acc.booking')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='acc.user')),
                ('serviceman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='acc.serviceman')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
