from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ProductForm, ReviewForm
from category.models import Category
from store.models import Product

# def category(request, foo):
#     foo = foo.replace('-', ' ')
#     category = get_object_or_404(Category, name__iexact=foo)
#     products = Product.objects.filter(category=category)
#     return render(request, 'products/category.html', {
#         'category': category,
#         'products': products,
#     })

def all_products(request):
    """Display all products, with optional search query."""
    products = Product.objects.all()
    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'products': products,
        'search_query': query,
    }
    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """Show product details and reviews."""
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()

    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """Add a product (superuser only)."""
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
    """Edit a product (superuser only)."""
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
    """Delete a product (superuser only)."""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('all_products'))


@login_required
def add_review(request, product_id):
    """Add a review for a product."""
    product = get_object_or_404(Product, pk=product_id)

    # Prevent multiple reviews by the same user
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, 'You have already submitted a review for this product.')
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
