from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm

def all_products(request):
    products = Product.objects.all()
    return render(request, 'products/all_products.html', {'products': products})
# def all_products(request):
#     """ A view to show all products, with sorting and search queries """
#     products = Product.objects.all()
#     query = None
#     categories = None
#     sort = None
#     direction = None

#     if request.GET:
#         if 'sort' in request.GET:
#             sortkey = request.GET['sort']
#             sort = sortkey
#             if sortkey == 'name':
#                 sortkey = 'lower_name'
#                 products = products.annotate(lower_name=Lower('name'))
#             if sortkey == 'category':
#                 sortkey = 'category__name'
#             if 'direction' in request.GET:
#                 direction = request.GET['direction']
#                 if direction == 'desc':
#                     sortkey = f'-{sortkey}'
#             products = products.order_by(sortkey)

#         if 'category' in request.GET:
#             categories = request.GET['category'].split(',')
#             products = products.filter(category__name__in=categories)
#             categories = Category.objects.filter(name__in=categories)

#         if 'q' in request.GET:
#             query = request.GET['q']
#             if not query:
#                 messages.error(request, "You didn't add any search criteria")
#                 return redirect(reverse('all_products'))

#             queries = Q(name__icontains=query) | Q(description__icontains=query)
#             products = products.filter(queries)

#     current_sorting = f'{sort}_{direction}' if sort else ''

#     context = {
#         'products': products,
#         'search_term': query,
#         'current_categories': categories,
#         'current_sorting': current_sorting,
#     }
#     return render(request, 'products/all_products.html', {'products': products})


def product_detail(request, product_id):
    """ A view to show product details """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please check the form.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please check the form.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('all_products'))


def add_review(request, product_id):
    """ Add a review for a product """
    product = get_object_or_404(Product, pk=product_id)

    # Prevent multiple reviews by the same user
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, 'You have already submitted a review for this product.')
        return redirect(reverse('product_detail', args=[product_id]))

    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to leave a review.')
        return redirect(reverse('product_detail', args=[product_id]))

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for submitting a review!')
            return redirect(reverse('product_detail', args=[product_id]))
    else:
        form = ReviewForm()

    return render(request, 'products/add_review.html', {'product': product, 'form': form})
