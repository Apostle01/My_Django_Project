from .cart import Cart

def cart_contents(request):
    """
    Makes cart data (items, count, total) available to all templates.
    """
    cart = Cart(request)
    total = cart.get_total_price()
    cart_items = list(cart)
    cart_item_count = len(cart)

    return {
        'cart_items': cart_items,
        'total': total,
        'cart_item_count': cart_item_count,
    }


# def cart_contents(request):
#     """
#     Safely return cart items and total cost for templates.
#     Works even if the cart data is malformed or uses integers instead of dicts.
#     """
#     cart = request.session.get('cart', {})
#     total = 0
#     cart_items = []

#     for item_id, item_data in cart.items():
#         # Case 1: modern structured cart format {'price': '10.00', 'quantity': 2}
#         if isinstance(item_data, dict):
#             price = float(item_data.get('price', 0))
#             quantity = int(item_data.get('quantity', 1))
#             total += price * quantity
#             cart_items.append({
#                 'id': item_id,
#                 'price': price,
#                 'quantity': quantity
#             })

#         # Case 2: legacy format (just a quantity integer)
#         elif isinstance(item_data, int):
#             # Optional: you could load the product from DB if needed
#             total += 0  # Skip price if not stored
#             cart_items.append({
#                 'id': item_id,
#                 'price': 0,
#                 'quantity': item_data
#             })

#     return {
#         'cart_items': cart_items,
#         'total': total
#     }
