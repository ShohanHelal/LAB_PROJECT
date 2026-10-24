from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Review(models.Model):
    """A customer's review of a provider, written after a completed job.
    One booking can have only one review."""

    RATING_CHOICES = [
        (5, '5 - Excellent'),
        (4, '4 - Good'),
        (3, '3 - Okay'),
        (2, '2 - Poor'),
        (1, '1 - Terrible'),
    ]

    booking = models.OneToOneField(
        'acc.Booking', on_delete=models.CASCADE, related_name='review'
    )
    customer = models.ForeignKey(
        'acc.User', on_delete=models.CASCADE, related_name='reviews'
    )
    serviceman = models.ForeignKey(
        'acc.Serviceman', on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer} -> {self.serviceman}: {self.rating}/5'

    def stars(self):
        """Example: rating 4 -> ★★★★☆"""
        return '★' * self.rating + '☆' * (5 - self.rating)
