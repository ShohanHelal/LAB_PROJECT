from django.db.models import Avg, Count
from django.shortcuts import render

from acc.models import Service, Location, Serviceman, User
from reviews.models import Review


def home(request):
    customer = User.objects.filter(
        id=request.session.get('customer_id')
    ).first()

    # best rated providers
    top_providers = Serviceman.objects.select_related(
        'service', 'location'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    ).order_by('-avg_rating', '-review_count')[:4]

    return render(request, 'Home.html', {
        'services': Service.objects.all(),
        'popular_services': Service.objects.exclude(image_url='')[:5],
        'locations': Location.objects.all(),
        'top_providers': top_providers,
        'latest_reviews': Review.objects.select_related(
            'customer', 'customer__location'
        )[:3],
        'my_location_id': customer.location_id if customer else None,
    })
