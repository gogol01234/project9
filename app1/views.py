from django.contrib.auth import login
from django.db.models.fields.json import JSONExact
from django.shortcuts import render, redirect
from django.views import View
from app1.models import Product, Customer, OrderedPlaced, Cart
from app1.forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
def home(request):
    totalitem = 0
    products = Product.objects.all()
    topwears = Product.objects.filter(category = "TW")
    bottomwears = Product.objects.filter(category = "BW")
    mobiles = Product.objects.filter(category = "M")
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    context = {
        "topwears":topwears,
        "mobiles":mobiles,
        "bottomwears":bottomwears,
        "products":products,
        "totalitem":totalitem
    }
    return render(request, "app1/home.html", context)

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {
            "form":form
            }
        
        return render(request, "app1/registration.html", context)
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation! Registered Successfully.")
            return redirect("/registration/")
        context = {
            "form":form
            }
        return render(request,"app1/registration.html", context)
@login_required
def cart(request):
    user = request.user
    product_id = request.GET.get("prod_id")
    product = Product.objects.get(id = product_id)
    cart = Cart(user = user, product = product)
    cart.save()
    return redirect("/add-to-cart/")
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user == user]
        if cart_product:
            for i in cart_product:
                tempamount = (i.quantity * i.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            totalitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user = request.user))
            context = {
                    "cart":cart,
                    "total_amount":total_amount,
                    "amount":amount,
                    "shipping_amount":shipping_amount,
                    "totalitem":totalitem
                    }  
            return render(request,"app1/cart.html", context)
        else:
            return render(request, "app1/empty.html")
def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity+= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user == request.user]
        for i in cart_product:
                tempamount = (i.quantity * i.product.discounted_price)
                amount += tempamount
        data = {
            "quantity":c.quantity,
            "amount":amount,
            "totalamount":amount+shipping_amount,
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity-= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user == request.user]
        for i in cart_product:
                tempamount = (i.quantity * i.product.discounted_price)
                amount += tempamount
        data = {
            "quantity":c.quantity,
            "amount":amount,
            "totalamount":amount+shipping_amount,
        }
        return JsonResponse(data)
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET["prod_id"]
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [i for i in Cart.objects.all() if i.user == request.user]
        for i in cart_product:
                tempamount = (i.quantity * i.product.discounted_price)
                amount += tempamount
        data = {
            "amount":amount,
            "totalamount":amount+shipping_amount,
        }
        return JsonResponse(data)
def delete_cart(request, pk = None):
    cart = Cart.objects.get(id = pk)
    cart.delete()
    return redirect("/add-to-cart/")

@method_decorator(login_required, name = "dispatch")
class profileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        context = {
            "form":form,
            "totalitem":totalitem
        }
        return render(request, "app1/profile.html", context)
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            locality = form.cleaned_data["locality"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            zipcode = form.cleaned_data["zipcode"]
            customer = Customer(user = user,name = name, locality = locality, city = city, state = state, zipcode = zipcode)
            customer.save()
            messages.success(request, "Congratulation! Profile Updated")
            totalitem = 0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user = request.user))

        context = {
            "form":form,
            "totalitem":totalitem
        }
        return render(request, "app1/profile.html", context)


@login_required        
def orders(request):
    totalitem = 0
    order = OrderedPlaced.objects.filter(user = request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    context = {
        "order":order,
        "totalitem":totalitem
    }
    return render(request, "app1/orders.html", context)


@login_required     
def address(request):
    add = Customer.objects.filter(user = request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    context = {
        "add":add,
        "totalitem":totalitem
    }
    return render(request, "app1/address.html", context)
@login_required 
def checkout(request):
    user = request.user
    cart = Cart.objects.filter(user = user)
    add = Customer.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [i for i in Cart.objects.all() if i.user == request.user]
    if cart_product:
        for i in cart_product:
            tempamount = (i.quantity * i.product.discounted_price)
            amount += tempamount
        total_amount = amount+shipping_amount
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
        context = {
                "cart":cart,
                "address":add,
                "amount":amount,
                "total_amount":total_amount,
                "totalitem":totalitem
                }
        return render(request, "app1/checkout.html",context)
    else:
        return redirect("/add-to-cart/")   
@login_required       
def paymentdone(request):
    user = request.user
    custid = request.GET.get("custid")
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user = user)
    for i in cart:
        OrderedPlaced(user = user, customer = customer, product = i.product, quantity = i.quantity).save()
        i.delete()
    return redirect("/orders/")

def product_detail(request, id):
    productdetails = Product.objects.get(id = id)
    totalitem = 0
    item_exist = False
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        item_exist = Cart.objects.filter(Q(product= productdetails.id) & Q(user = request.user)).exists()

    context = {
        "productdetails":productdetails,
        "item_exist":item_exist,
        "totalitem":totalitem
    }
    return render(request, "app1/product_detail.html", context)

def mobiles(request, data = None):
    totalitem = 0
    if data == None:
        mobiles = Product.objects.filter(category = "M")
    elif data == "Redmi" or data == "Vivo" or data == "Samsung":
        mobiles = Product.objects.filter(category = "M").filter(brand = data)
    elif data == "below":
        mobiles = Product.objects.filter(category = "M").filter(discounted_price__lt = 10000)
    elif data == "above":
        mobiles = Product.objects.filter(category = "M").filter(discounted_price__gt = 10000)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))    
    
    context = {
        "mobiles":mobiles,
        "totalitem":totalitem
    }
    return render(request, "app1/mobiles.html", context)

def top_wears(request, data = None):
    totalitem = 0
    if data == None:
        top_wears = Product.objects.filter(category = "TW")
    elif data == "Nike" or data == "Gucci" or data == "everlance":
        top_wears = Product.objects.filter(category = "TW").filter(brand = data)
    elif data == "below":
        top_wears = Product.objects.filter(category = "TW").filter(discounted_price__lt = 1000)
    elif data == "above":
        top_wears = Product.objects.filter(category = "TW").filter(discounted_price__gt = 1000)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
    context = {

        "top_wears":top_wears,
        "totalitem":totalitem
    }
    return render(request, "app1/top_wears.html", context)
def bottom_wears(request, data = None):
    if data == None:
        bottom_wears = Product.objects.filter(category = "BW")
    elif data == "Wragler" or data == "Lee" or data == "Guess":
        bottom_wears = Product.objects.filter(category = "BW").filter(brand = data)
    elif data == "below":
        bottom_wears = Product.objects.filter(category = "BW").filter(discounted_price__lt = 1000)
    elif data == "above": 
        bottom_wears = Product.objects.filter(category = "BW").filter(discounted_price__gt = 1000)
   
    context = {

        "bottom_wears":bottom_wears,
    
    }
    return render(request, "app1/bottom_wears.html", context)
#def laptop(request, data = None):
    #if data == None:
        #laptops = Product.objects.filter(category = "L")
    #elif data == ""
    #return render(request, "app1/laptop.html")getsomehelp1
