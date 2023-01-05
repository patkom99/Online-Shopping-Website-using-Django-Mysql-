from django.urls import path
from account import views as v

urlpatterns = [
    path("Reg",v.reg,name="reg"),
    path("Login",v.logi,name="loginpage"),
    path("Logout",v.logt,name="logout"),
    
    path("edit/<int:id>",v.edit,name="edit"),

    path("collections",v.collections,name="collections"),
    path("products/<str:slug>",v.productsview,name="productsview"),
    path("product/<str:cate_slug>/<str:prod_slug>",v.productview,name="productview"),

    path('add-to-cart',v.addtocart,name="addtocart"),
    path('cart',v.viewcart, name="cart"),
    path("deletecart/<int:id>",v.deletecart,name="deletecart"),
    path("update-cart",v.updatecart,name="updatecart"),

    path('add-to-wishlist',v.addtowishlist,name="addtowishlist"),
    
    path("wishlist",v.wishlist,name="wishlist"),
    path("deletewishlist/<int:id>",v.deletewishlist,name="deletewishlist"),
    path("checkout",v.checkoutview,name="checkout"),
    path('place-order',v.placeorder,name="placeorder"),

    path("my-orders", v.myorders,name="myorders"),
    path("view-order/<str:t_no>",v.vieworder,name="orderview"),

    path('proceed-to-pay',v.razorpaycheck)

]

