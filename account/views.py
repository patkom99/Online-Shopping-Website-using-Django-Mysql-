from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from account.models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import random

def home(request):
    trending_products=Product.objects.filter(trending=1)
    d={'trending_products':trending_products}
    return render(request,"home.html",d)


def reg(request):
    if request.method == "POST":
        obj = RegForm(request.POST)
        obj.save()
        messages.success(
            request, "Your account has been successfully created...!!")
        return redirect("/ACCOUNT-Login")
    else:
        d = {"form": RegForm}
        return render(request, "register.html", d)


def logi(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            request.session["uid"] = user.id
            login(request, user)
            messages.success(request, "Logged In Successfully..!!!")
            return redirect("/")
        else:
            messages.error(request, "Invalid username & password..!!!")
            return redirect("/ACCOUNT-Login")
    else:
        d = {"form": LoginForm}
        return render(request, "login.html", d)


def logt(request):
    logout(request)
    messages.success(request, "Logged Out successfully...!!!")
    return redirect("/")


def collections(request):
    category = Category.objects.all
    return render(request, "collection.html", {'category': category})


def productsview(request, slug):
    if (Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        category = Category.objects.filter(slug=slug).first()
        d = {"products": products, "category": category}
        return render(request, "products.html", d)
    else:
        messages.warning(request, "No such category found")
        return redirect("/ACCOUNT-collections")


def productview(request, cate_slug, prod_slug):
    if (Category.objects.filter(slug=cate_slug)):
        if (Product.objects.filter(slug=prod_slug)):
            products = Product.objects.filter(slug=prod_slug).first()
            d = {"products": products}
        else:
            messages.error(request, "No such Product found")
            return redirect("/ACCOUNT-collections")
    else:
        messages.error(request, "No such category found")
        return redirect("/ACCOUNT-collections")
    return render(request, "productview.html", d)


def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if (product_check):
                if (Cart.objects.filter(user=request.user.id, product_id=prod_id)):
                    
                    return JsonResponse({'status': "Product already in cart"})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        return JsonResponse({'status': "Product added successfully"})
                    else:
                        return JsonResponse({'status': "Only "+str(product_check.quantity) + " quantity available"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect("/")

def addtowishlist(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            if (product_check):
                if (Wishlist.objects.filter(user=request.user, product_id=prod_id)):                   
                    return JsonResponse({'status': "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status': "Product added to wishlist"})
            else:
                return JsonResponse({'status': "No such product found"})
        else:
            return JsonResponse({'status': "Login to Continue"})
    return redirect("/")

def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    d = {'cart': cart}
    return render(request, "cart.html", d)


def deletecart(request, id):
    obj = Cart.objects.get(id=id)
    obj.delete()
    return redirect("/ACCOUNT-cart")


def edit(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        obj = RegForm(request.POST, instance=user)
        obj.save()
        messages.success(
            request, "Your profile has been successfully updated...!!!")
        return redirect("/")
    else:
        x = RegForm(instance=user)
        d = {"form": x}
        return render(request, "edituser.html", d)

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user, product_id=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product_id=prod_id, user=request.user)
            cart.product_qty = prod_qty
            cart.save()
            return JsonResponse({'status':"Updated successfully"})
    return redirect("/")

def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    d={'wishlist':wishlist}
    return render(request,"wishlist.html",d)

def deletewishlist(request, id):
    obj = Wishlist.objects.get(id=id)
    obj.delete()
    return redirect("/ACCOUNT-wishlist")


def checkoutview(request):
    rawcart=Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity:
            abc = Cart.objects.get(id=item.id)
            abc.delete()

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()

    d={'cartitems': cartitems, 'total_price':total_price,"userprofile":userprofile}
    return render(request, "checkout.html",d)

def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user   
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        cart=Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'BRO'+str(random.randint(1111111,99999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'BRO'+str(random.randint(1111111,99999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your order has been placed successfully")

    return redirect('/')

def myorders(request):
    orders = Order.objects.filter(user=request.user)
    d={'orders':orders}
    return render(request,"orders.html",d)

def vieworder(request, t_no):
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    d={'order':order,'orderitems':orderitems}
    return render(request,"vieworder.html",d)

def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price': total_price
    })