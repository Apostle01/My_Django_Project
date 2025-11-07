from django.shortcuts import (
    render,
    redirect,
    get_object_or_404    
)
from django.http import HttpResponse
from django.urls import reverse
from products.models import Product
from django.contrib import messages

def view_bag(request):
    """ View to show the contents of the shoppers bag """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url')
    size = None

    # Handle product with size options (if applicable)
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    # Get the bag from session or create a new one
    bag = request.session.get('bag', {})

    if size:
        if item_id in bag:
            if size in bag[item_id]['items_by_size']:
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in bag:
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    messages.success(request, f'Added {product.name} to your bag')
    return redirect('view_bag')

def adjust_bag(request, item_id):
    """Adjust the quantity of products within the bag"""

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))

    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request,
            f'Updated {product.name} quantity to {bag[item_id]}'
            )
    else:
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
    Remove product from bag    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item {e} ')
        return HttpResponse(status=500)
