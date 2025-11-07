# checkout/views.py
from decimal import Decimal
import json

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from products.models import Product
from .forms import OrderForm
from .models import Order, OrderLineItem

import stripe


@require_POST
def cache_checkout_data(request):
    """
    Optional: caches data against the PaymentIntent (metadata).
    Keep this if you use an AJAX endpoint to attach session data to the PaymentIntent.
    """
    try:
        client_secret = request.POST.get("client_secret", "")
        pid = client_secret.split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY or ""
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(request.session.get("bag", {})),
                "save_info": request.POST.get("save_info", ""),
                "username": str(request.user),
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Sorry — we couldn't process your payment right now.")
        return HttpResponse(content=str(e), status=400)


def _compute_bag_from_session(request):
    """
    Helper to read request.session['bag'] and return bag_items, totals, counts, delivery.
    Bag format expected:
      bag = {
        "<product_id>": <int quantity>    # product without sizes
        "<product_id>": {"items_by_size": {"S": 1, "M": 2}},  # product with sizes
      }
    NOTE: Any key named 'delivery' is ignored.
    """
    bag = request.session.get("bag", {})
    bag_items = []
    total = Decimal("0.00")
    product_count = 0

    for item_id, item_data in bag.items():
        # Skip any non-product keys saved accidentally
        if str(item_id).lower() == "delivery":
            continue

        # item_id might be stored as string — convert to int safely
        try:
            product = Product.objects.get(pk=int(item_id))
        except (Product.DoesNotExist, ValueError, TypeError):
            # skip invalid ids (e.g. stray keys)
            continue

        if isinstance(item_data, int):
            qty = item_data
            total += Decimal(qty) * Decimal(product.price)
            product_count += qty
            bag_items.append({
                "item_id": item_id,
                "quantity": qty,
                "product": product,
            })
        else:
            # expect dict with 'items_by_size'
            items_by_size = item_data.get("items_by_size", {})
            for size, quantity in items_by_size.items():
                qty = int(quantity)
                total += Decimal(qty) * Decimal(product.price)
                product_count += qty
                bag_items.append({
                    "item_id": item_id,
                    "quantity": qty,
                    "product": product,
                    "size": size,
                })

    # Delivery calculations from settings
    free_delivery_threshold = Decimal(str(getattr(settings, "FREE_DELIVERY_THRESHOLD", "250.00")))
    standard_delivery_percentage = Decimal(str(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", "20")))

    if total < free_delivery_threshold and total != Decimal("0.00"):
        delivery = (total * standard_delivery_percentage / Decimal("100")).quantize(Decimal("0.01"))
        free_delivery_delta = (free_delivery_threshold - total).quantize(Decimal("0.01"))
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = (total + delivery).quantize(Decimal("0.01"))

    return {
        "bag_items": bag_items,
        "total": total.quantize(Decimal("0.01")),
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": free_delivery_threshold,
        "grand_total": grand_total,
    }


def checkout(request):
    """
    Full checkout view: calculates bag data, shows order form, and creates Stripe PaymentIntent.
    """
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")

    # Recompute bag / totals
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("all_products"))

    bag_context = _compute_bag_from_session(request)
    bag_items = bag_context["bag_items"]
    total = bag_context["total"]
    delivery = bag_context["delivery"]
    free_delivery_delta = bag_context["free_delivery_delta"]
    free_delivery_threshold = bag_context["free_delivery_threshold"]
    grand_total = bag_context["grand_total"]
    product_count = bag_context["product_count"]

    # Save delivery (string) in session if you really want to keep it, but avoid using it as product id
    # It's safer to store metadata separately - if you must:
    request.session.setdefault("bag_meta", {})
    request.session["bag_meta"]["delivery"] = str(delivery)

    # POST handling: create Order and OrderLineItems
    if request.method == "POST":
        form_data = {
            "full_name": request.POST.get("full_name", ""),
            "email": request.POST.get("email", ""),
            "phone_number": request.POST.get("phone_number", ""),
            "country": request.POST.get("country", ""),
            "postcode": request.POST.get("postcode", ""),
            "town_or_city": request.POST.get("town_or_city", ""),
            "street_address1": request.POST.get("street_address1", ""),
            "street_address2": request.POST.get("street_address2", ""),
            "county": request.POST.get("county", ""),
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret", "").split("_secret")[0] if request.POST.get("client_secret") else ""
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.order_total = total
            order.delivery_cost = delivery
            order.grand_total = grand_total
            order.save()

            # create line items using the precomputed bag_items list
            for item in bag_items:
                try:
                    if "size" in item:
                        OrderLineItem.objects.create(
                            order=order,
                            product=item["product"],
                            quantity=item["quantity"],
                            product_size=item["size"],
                        )
                    else:
                        OrderLineItem.objects.create(
                            order=order,
                            product=item["product"],
                            quantity=item["quantity"],
                        )
                except Exception:
                    messages.error(request, "Problem adding an item to your order. Please contact support.")
                    order.delete()
                    return redirect(reverse("view_bag"))

            request.session["save_info"] = "save-info" in request.POST
            return redirect(reverse("checkout_success", args=[order.order_number]))
        else:
            messages.error(request, "There was an error with your form. Please double check your information.")
    else:
        # populate form for a logged-in user
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    "full_name": f"{request.user.first_name} {request.user.last_name}".strip(),
                    "email": request.user.email,
                    "phone_number": profile.default_phone_number,
                    "country": profile.default_country,
                    "postcode": profile.default_postcode,
                    "town_or_city": profile.default_town_or_city,
                    "street_address1": profile.default_street_address1,
                    "street_address2": profile.default_street_address2,
                    "county": profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    # Create Stripe PaymentIntent (only if keys available)
    intent = None
    try:
        if not stripe_secret_key:
            raise ValueError("Missing Stripe secret key.")
        stripe.api_key = stripe_secret_key
        stripe_total = int(grand_total * 100)  # integer cents
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=getattr(settings, "STRIPE_CURRENCY", "usd"),
        )
    except Exception as e:
        # If Stripe fails, show a warning but still render the page so user can correct bag/form
        messages.warning(request, f"Stripe error: {e}. Use admin to set valid keys.")

    context = {
    'order_form': order_form,
    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    'client_secret': intent.client_secret,
    'bag_items': bag_items,
    'total': total,
    'delivery': delivery,
    'grand_total': grand_total,
    'free_delivery_delta': free_delivery_delta,
    'product_count': product_count,
}
    return render(request, "checkout/checkout.html", context)


# from decimal import Decimal
# from django.shortcuts import render, redirect, reverse, get_object_or_404
# from django.http import HttpResponse
# from django.views.decorators.http import require_POST
# from django.contrib import messages
# from django.conf import settings
# from profiles.models import UserProfile
# from profiles.forms import UserProfileForm
# from products.models import Product
# from .forms import OrderForm
# from .models import Order, OrderLineItem
# import stripe
# import json

# @require_POST
# def cache_checkout_data(request):
#     """Cache checkout data in Stripe payment metadata."""
#     try:
#         pid = request.POST.get("client_secret").split("_secret")[0]
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         stripe.PaymentIntent.modify(
#             pid,
#             metadata={
#                 "bag": json.dumps(request.session.get("bag", {})),
#                 "save_info": request.POST.get("save_info"),
#                 "username": str(request.user),
#             },
#         )
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, "Sorry, your payment cannot be processed right now. Please try again later.")
#         return HttpResponse(content=str(e), status=400)


# from decimal import Decimal
# from django.conf import settings
# from django.shortcuts import render, redirect, reverse, get_object_or_404
# from django.contrib import messages
# from products.models import Product
# from .forms import OrderForm
# from .models import OrderLineItem
# from profiles.models import UserProfile
# import stripe
# import json

# def checkout(request):
#     """Handle checkout page with bag totals, delivery, and Stripe."""
#     stripe_public_key = settings.STRIPE_PUBLIC_KEY
#     stripe_secret_key = settings.STRIPE_SECRET_KEY

#     # Get bag from session
#     session_bag = request.session.get("bag", {})

#     # ✅ Remove any non-product keys before processing
#     bag = {
#         key: value for key, value in session_bag.items()
#         if key.isdigit()  # keep only numeric keys (product IDs)
#     }

#     if not bag:
#         messages.error(request, "There's nothing in your bag at the moment.")
#         return redirect(reverse("all_products"))

#     # --- Calculate totals ---
#     bag_items = []
#     total = Decimal("0.00")
#     product_count = 0

#     # ✅ Only product IDs remain here
#     for item_id, item_data in bag.items():
#         try:
#             product = Product.objects.get(pk=int(item_id))
#         except (Product.DoesNotExist, ValueError):
#             continue

#         if isinstance(item_data, int):
#             total += item_data * product.price
#             product_count += item_data
#             bag_items.append({
#                 "item_id": item_id,
#                 "quantity": item_data,
#                 "product": product,
#             })
#         else:
#             for size, quantity in item_data.get("items_by_size", {}).items():
#                 total += quantity * product.price
#                 product_count += quantity
#                 bag_items.append({
#                     "item_id": item_id,
#                     "quantity": quantity,
#                     "product": product,
#                     "size": size,
#                 })

#     # --- Delivery calculations ---
#     free_delivery_threshold = Decimal(str(getattr(settings, "FREE_DELIVERY_THRESHOLD", 250.00)))
#     standard_delivery_percentage = Decimal(str(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 20)))

#     if total < free_delivery_threshold:
#         delivery = total * standard_delivery_percentage / 100
#         free_delivery_delta = free_delivery_threshold - total
#     else:
#         delivery = Decimal("0.00")
#         free_delivery_delta = Decimal("0.00")

#     grand_total = total + delivery

#     # ✅ Store delivery separately (not inside the "bag" items)
#     request.session["delivery"] = str(delivery)

#     # --- Handle POST form submission ---
#     if request.method == "POST":
#         form_data = {
#             "full_name": request.POST.get("full_name"),
#             "email": request.POST.get("email"),
#             "phone_number": request.POST.get("phone_number"),
#             "country": request.POST.get("country"),
#             "postcode": request.POST.get("postcode"),
#             "town_or_city": request.POST.get("town_or_city"),
#             "street_address1": request.POST.get("street_address1"),
#             "street_address2": request.POST.get("street_address2"),
#             "county": request.POST.get("county"),
#         }
#         order_form = OrderForm(form_data)
#         if order_form.is_valid():
#             order = order_form.save(commit=False)
#             pid = request.POST.get("client_secret").split("_secret")[0]
#             order.stripe_pid = pid
#             order.original_bag = json.dumps(bag)
#             order.save()

#             for item in bag_items:
#                 try:
#                     if "size" in item:
#                         OrderLineItem.objects.create(
#                             order=order,
#                             product=item["product"],
#                             quantity=item["quantity"],
#                             product_size=item["size"],
#                         )
#                     else:
#                         OrderLineItem.objects.create(
#                             order=order,
#                             product=item["product"],
#                             quantity=item["quantity"],
#                         )
#                 except Product.DoesNotExist:
#                     messages.error(request, "One of the products in your bag wasn't found in our database.")
#                     order.delete()
#                     return redirect(reverse("view_bag"))

#             request.session["save_info"] = "save-info" in request.POST
#             return redirect(reverse("checkout_success", args=[order.order_number]))
#         else:
#             messages.error(request, "Please correct the errors in the form.")
#     else:
#         # Pre-fill form if user logged in
#         if request.user.is_authenticated:
#             try:
#                 profile = UserProfile.objects.get(user=request.user)
#                 order_form = OrderForm(initial={
#                     "full_name": f"{request.user.first_name} {request.user.last_name}".strip(),
#                     "email": request.user.email,
#                     "phone_number": profile.default_phone_number,
#                     "country": profile.default_country,
#                     "postcode": profile.default_postcode,
#                     "town_or_city": profile.default_town_or_city,
#                     "street_address1": profile.default_street_address1,
#                     "street_address2": profile.default_street_address2,
#                     "county": profile.default_county,
#                 })
#             except UserProfile.DoesNotExist:
#                 order_form = OrderForm()
#         else:
#             order_form = OrderForm()

#     # --- Stripe PaymentIntent ---
#     stripe.api_key = stripe_secret_key
#     stripe_total = round(grand_total * 100)
#     intent = stripe.PaymentIntent.create(
#         amount=stripe_total,
#         currency=settings.STRIPE_CURRENCY,
#     )

#     context = {
#         "order_form": order_form,
#         "bag_items": bag_items,
#         "total": total,
#         "delivery": delivery,
#         "grand_total": grand_total,
#         "product_count": product_count,
#         "free_delivery_delta": free_delivery_delta,
#         "free_delivery_threshold": free_delivery_threshold,
#         "stripe_public_key": stripe_public_key,
#         "client_secret": intent.client_secret,
#     }

#     return render(request, "checkout/checkout.html", context)

def checkout_success(request, order_number):
    """Handle successful checkouts."""
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        f"Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.",
    )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/checkout_success.html"
    context = {"order": order}

    return render(request, template, context)
