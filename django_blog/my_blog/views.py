
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, ImageUpload, Category, FavouriteModel
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse
from django.urls import reverse, NoReverseMatch
from itertools import cycle
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "products": page_obj,
        "categories": categories,
    }
    return render(request, 'product_list.html', context)


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    product_category = product.category
    related_products = Product.objects.filter(category=product_category).exclude(id=id)[:4]
    all_products = list(Product.objects.exclude(id=id))
    
    if all_products:
        current_product_index = request.session.get('current_product_index', 0)
        all_products_iterator = cycle(all_products)
        for _ in range(current_product_index + 1):
            another_product_id = next(all_products_iterator, None)
            another_product = get_object_or_404(Product, id=another_product_id.id) if another_product_id is not None else None

        request.session['current_product_index'] = (current_product_index + 1) % len(all_products)
    else:
        another_product = None

    images = ImageUpload.objects.filter(product=product)
    
    context = {
        "product": product,
        "images": images,
        "related_products": related_products,
        "another_product": another_product,
    }

    # Reversing the URL with product.id instead of product.name
    try:
        context["current_product_details_url"] = reverse('product_details', kwargs={'id': product.id})
    except NoReverseMatch:
        context["current_product_details_url"] = None

    return render(request, 'product_details.html', context)


@permission_required('my_blog.add_productmodel', login_url='/login/')
def create_product(request):
    if request.method == "GET":
        category = Category.objects.all()
        return render(request, 'create_product.html', {'category': category})
    if request.method == 'POST':
        # Create the product instance
        product = Product.objects.create(
            user=request.user, 
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            model_date=request.POST.get('model_date'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            category_id=request.POST.get('category'),
        )

        # Handle multiple images
        images = request.FILES.getlist('images')
        for img in images:
            # Create ImageUpload instance and associate it with the product
            image_instance = ImageUpload.objects.create(product=product, image=img)
        messages.success(request, "The post has been created successfully.")
        return redirect('product_list')

    return render(request, 'create_product.html')


def delete_product(request, id=None):
    try:
        if id is not None:
            product = Product.objects.get(id=id)

            # Check if there are any related images
            images = ImageUpload.objects.filter(product=product)
            
            if images.exists():
                # Delete individual images
                for image in images:
                    image.image.delete()
                    image.delete()

                # Delete the product
                product.thumbnail.delete()
                product.delete()

                messages.success(request, "The post has been deleted successfully.")
            else:
                messages.warning(request, "No images found for the product.")
        else:
            messages.warning(request, "Product ID is missing.")

    except Product.DoesNotExist:
        messages.warning(request, "The specified product does not exist.")
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")

    return redirect('product_list')


def add_category(request):
    if request.method == "GET":
        return render(request, 'add_category.html')
    if request.method == "POST":
        category = Category.objects.create(
            name = request.POST.get('add_category')
            )
        category.save()
        messages.success(request, "The category has been added successfully.")
        return redirect('create_product')


def product_list_category(request, category=None):
    if category:
        # Filter products by category if a category is provided
        products = Product.objects.filter(category__name=category).order_by('-id')
    else:
        # Show all products if no category is provided
        products = Product.objects.all().order_by('-id')

    categories = Category.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "selected_category": category,
    }

    return render(request, 'product_list.html', context)


@login_required(login_url='/login/')
def add_favourite(request, product_id):
    # Check if the product is already in favorites
    if FavouriteModel.objects.filter(product_id=product_id, user=request.user).exists():
        # Product is already in favorites, handle accordingly (e.g., display a message)
        messages.info(request, 'This bike is already in your favorites.')
    else:
        # Product is not in favorites, add it
        favourite = FavouriteModel.objects.create(
            product=Product.objects.get(id=product_id),
            qty=request.GET.get('qty'),
            user=request.user,
            created_at=datetime.now()
        )
        favourite.save()
        messages.success(request, 'The bike has been added to favorites successfully.')

    return redirect(f'/product/details/{product_id}')


@login_required(login_url='/login/')
def remove_favourite(request, product_id):
    try:
        # Filter the favorite entries by product_id and user
        favourites = FavouriteModel.objects.filter(product_id=product_id, user=request.user)
        
        # Check if any matching favorite entries exist
        if favourites.exists():
            # Delete all matching favorite entries (you may want to refine this logic based on your requirements)
            favourites.delete()
            messages.success(request, 'The product has been removed from favorites successfully.')
        else:
            messages.info(request, 'This product is not in your favorites.')
    except FavouriteModel.DoesNotExist:
        # Handle the case where no favorite entries are found
        messages.info(request, 'This product is not in your favorites.')

    return redirect('favourite_product')
 

@login_required
def favourite_product(request):
    # Filter by the currently authenticated user
    favourites = FavouriteModel.objects.filter(user=request.user)

    return render(request, 'favourite_product.html', {'favourites': favourites})


def search_by(request):
    search = request.GET.get('search')
    if search:
        products = Product.objects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
        return render(request, 'product_list.html', {'products': products})
    else:
        # Assuming PostModel is not defined, you might want to change this to your actual model
        products = Product.objects.all().order_by('-created_at')
        return render(request, 'product_list.html', {'products': products})


def RegisterView(request):
    if request.method == "GET":
        return render(request, 'register.html')
    if request.method == "POST":
        if request.POST.get('password') == request.POST.get('repassword'):
            users = User.objects.create(
                username = request.POST.get('name'),
                email = request.POST.get('email'),
                password = make_password(request.POST.get('password'))
            )
            messages.success(request, "register success.")
            return redirect('/login/')
        else:
            messages.error(request, "Password is not same!")
            return redirect('/register/')


def loginView(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully.")
            return redirect('product_list')
        else:
            messages.error(request, "Username or password incorrect")
            return render(request, 'login.html')


def logoutView(request):
    logout(request)
    return redirect('/login/')



