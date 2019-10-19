from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.all().filter(product=product)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.product = product
        review.save()

        request.session['reviewed_products'].append(pk)
        request.session.modified = True

        is_review_exist = True
        form = None
    else:
        if pk in request.session['reviewed_products']:
            is_review_exist = True
            form = None
        else:
            is_review_exist = False
            form = ReviewForm()

    context = {
        'form': form,
        'product': product,
        'is_review_exist': is_review_exist,
        'reviews': reviews
    }

    return render(request, template, context)
