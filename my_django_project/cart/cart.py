from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        """Add or update the quantity of a product in the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        """Mark session as modified to ensure it's saved."""
        self.session.modified = True

    def __iter__(self):
        """Iterate through cart items and attach product objects."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            quantity = self.cart[str(product.id)]
            yield {
                'product': product,
                'quantity': quantity,
                'price': product.price,
                'total_price': product.price * quantity
            }

    def __len__(self):
        """Count total number of items in cart."""
        return sum(self.cart.values())

    def get_total_price(self):
        """Compute total price of all items."""
        total = Decimal(0)
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            quantity = self.cart[str(product.id)]
            total += Decimal(product.price) * quantity
        return total

    def clear(self):
        """Remove cart from session."""
        self.session['cart'] = {}
        self.save()
