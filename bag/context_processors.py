from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """Make bag data available across all templates"""
    bag_items = []
    total = Decimal('0.00')
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        try:
            product = Product.objects.get(pk=item_id)
        except Product.DoesNotExist:
            continue
        if isinstance(item_data, int):
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })
        

    # Use your free delivery threshold from settings or set a fallback
    free_delivery_threshold = getattr(settings, 'FREE_DELIVERY_THRESHOLD', Decimal('250.00'))
    free_delivery_threshold = Decimal(str(free_delivery_threshold))

    if total < free_delivery_threshold:
        free_delivery_delta = free_delivery_threshold - total
    else:
        free_delivery_delta = Decimal('0.00')

    grand_total = total

    return {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': free_delivery_threshold,
    }

    return context

