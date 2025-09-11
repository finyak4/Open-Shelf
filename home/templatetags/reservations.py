from django import template
from library.models import Reservation
from borrowings.models import Borrowing

register = template.Library()

@register.filter
def has_reserved(user):
    if not user.is_authenticated:
        return False
    return Reservation.objects.filter(user=user, handed=False).exists() or Borrowing.objects.filter(user=user).exists()