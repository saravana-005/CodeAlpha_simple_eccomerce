from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product,Cart,CartItem,Order,OrderItem
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .ai.smart_search import extract_filters
from django.contrib import messages
from datetime import timedelta,date
import random

@login_required
def home(request):
    return render(request,"home.html")

@login_required
def product_list(request,category=None):
    products=Product.objects.all()
    if category:
        products = Product.objects.filter(category=category)
    return render(request,"men.html",{"products":products})

def search_products(request):
    q=request.GET.get("q")
    if q:
       products = Product.objects.filter(Q(name__icontains=q)|Q(price__icontains=q)|Q(category__icontains=q))
    else:
      products=[]
        
    return render(request,"men.html",{'products':products,'query':q})

def smart_search(request):
    query = request.GET.get("q","")
    products = []

    if query:
        filters = extract_filters(query)
        products = Product.objects.filter(**filters) 

    return render (request,"men.html",{
        "products":products,
        "query":query
    })       

def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)

    cart,created = Cart.objects.get_or_create(user=request.user)
    item,created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
        )
    if not created:
        item.quantity +=1
    item.save()
    return redirect("view_cart")    

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    items = cart.items.all() if cart else []
    return render(request,"cart.html",{"items":items})

def increase(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    item.quantity +=1
    item.save()
    return redirect("view_cart")    

def decrease(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    if item.quantity>1:
        item.quantity -=1
        item.save()
    else:
        item.delete()    
    return redirect("view_cart")    

def remove(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    item.delete()    
    return redirect("view_cart")    

def register_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        confirm=request.POST['confirm']

        if password != confirm:
            return HttpResponse("Miss match password,TRY AGAIN")
        else:
            user=User.objects.create_user(username=username,password=password)
            return redirect('login')    
    else:
        return render(request,'register.html')    

def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("login failed")    
    else:
        return render(request,'login.html')    
    
@login_required
def place_order(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty")
        return redirect("view_cart")

    # 🎲 Random delivery date (3–7 days)
    delivery_date = date.today() + timedelta(days=random.randint(3, 7))

    order = Order.objects.create(
        user=request.user,
        delivery_date=delivery_date
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # 🧹 Clear cart
    cart.items.all().delete()

    messages.success(
        request,
        f"Order confirmed! Delivery by {delivery_date}"
    )

    return redirect("order_success")

@login_required
def order_success(request):
    return render(request, "order_success.html")


