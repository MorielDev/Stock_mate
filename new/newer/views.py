from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Profile, Inventory
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

# Existing views

def signup(request):
    if request.method == 'POST':
        username = request.POST['username'] # Gets the value of the data using the name of the input
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:  # If the user is in our db
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'INVALID CREDENTIALS')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def add(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        category = request.POST['category']
        stock = request.POST['stock']
        price = request.POST['price']

        # Create new Inventory object and save to DB
        new_item = Inventory.objects.create(item_name=item_name, category=category, stock=stock, price=price)
        new_item.save()

        return redirect('home')
    else:
        return render(request, 'add.html')

@login_required(login_url='signin')
def home(request):
    # Retrieve all products from the Inventory model
    products = Inventory.objects.all()

    # Pass the products to the template
    return render(request, 'home.html', {'products': products})

@login_required(login_url='signin')
def edit(request, item_id):
    # Retrieve the specific item using its ID (or another unique field)
    item = get_object_or_404(Inventory, pk=item_id)

    if request.method == 'POST':
        # Extract fields from POST data
        item_name = request.POST['item_name']
        category = request.POST['category']
        stock = request.POST['stock']
        price = request.POST['price']

        # Update item details
        item.item_name = item_name
        item.category = category
        item.stock = stock
        item.price = price
        item.save()

        return HttpResponse("Inventory updated successfully!")
        
    return render(request, 'edit.html', {'item': item})

@login_required(login_url='signin')
def categories(request):
    categories = Inventory.objects.values('category').distinct()
    return render(request, 'categories.html', {'categories': categories})

@login_required(login_url='signin')
def dashboard(request):
    # Data aggregation
    total_products = Inventory.objects.count()  # Total number of products
    total_stock = Inventory.objects.aggregate(Sum('stock'))['stock__sum'] or 0  # Total stock count
    low_stock = Inventory.objects.filter(stock__lt=10).count()  # Low stock items (<10)
    categories_count = Inventory.objects.values('category').annotate(count=Count('category')).order_by('-count')  # Count by category

    # For a chart or graph (example sales data)
    sales_data = Inventory.objects.values('category').annotate(total_stock=Sum('stock')).order_by('-total_stock')

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock': low_stock,
        'categories_count': categories_count,
        'sales_data': sales_data,
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='signin')
def profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'profile.html', {'profile': profile})

@login_required(login_url='signin')
def my_stocks(request):
    user = request.user
    stocks = Inventory.objects.filter(user=user)
    return render(request, 'viewStocks.html', {'stocks': stocks})
