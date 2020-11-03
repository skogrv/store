from django import http
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Listing, Comment, ListingImage
from .forms import CommentForm, ListingForm


@login_required
def home(request):
    return render(request, 'store/base.html', {})

@login_required
def create_listing(request):
    if request.method == 'POST':
        length = request.POST.get('length')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')

        order = Listing.objects.create(
            title=title,
            description=description,
            price=price

        )
        order.save()

        for file_num in range(0, int(length)):
            listing_image = ListingImage.objects.create(
                listing=order,
                images=request.FILES.get(f'images{file_num}')
            )
            listing_image.save()

    return render(request, 'store/create_view.html')



def delete_order(request, id):
    order_to_delete = get_object_or_404(Listing, id=id)
    if request.method =="POST":
        order_to_delete.delete()
        return redirect('listings')
    return render(request, "store/delete_order.html")

class EditOrder(UpdateView):
    template_name = 'store/edit_order.html'
    fields = ('title', 'description')
    model = Listing
    success_url = 'listings'


def listings(request):
    orders = Listing.objects.all()
    listing_images = ListingImage.objects.all()
    return render(request, 'store/listings.html', {'orders': orders, 'listing_images': listing_images})


def order_detail(request, id):
    order = get_object_or_404(Listing, id=id)
    photos = ListingImage.objects.filter(listing=order)
    comments = Comment.objects.filter(post=order).order_by('-created_on')
    paginator = Paginator(comments, 2)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    is_auth = False
    is_fav = False
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('comment')
            length = request.POST.get('length')
            ratings = request.POST.get('rating')
            comment = Comment.objects.create(post=order, comment=content, author=request.user, rating=ratings)
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        comment_form = CommentForm()
    if order.favourite.filter(id=request.user.id).exists():
        is_fav = True
    context = {
        'order': order,
        'comment_form': comment_form,
        'comments': comments,
        'is_favourite': is_fav,
        'page_obj': page_obj,
        'photos': photos
    }
    return render(request, 'store/order.html', context)


def favourite(request, id):
    order = get_object_or_404(Listing, id=id)
    if order.favourite.filter(id=request.user.id).exists():
        order.favourite.remove(request.user)
    else:
        order.favourite.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def like(request, id):
    comment_liked = get_object_or_404(Comment, id=id)
    if comment_liked.liked.filter(id=request.user.id).exists():
        comment_liked.liked.remove(request.user)
        comment_liked.is_liked = False
    else:
        comment_liked.liked.add(request.user)
        comment_liked.is_liked = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def favourite_list(request):
    user = request.user
    fav_orders = user.favourite.all()
    listing_images = ListingImage.objects.all()
    context = {
        'fav_orders': fav_orders,
        'listing_images': listing_images
    }
    return render(request, 'store/favourite_orders.html', context)


def delete_comment(request, pk):
    order = Comment.objects.get(pk=pk)
    order.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
