from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Category(models.Model):
    slug=models.CharField(max_length=150)
    name=models.CharField(max_length=150)
    image=models.ImageField(upload_to="myimages")
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False,help_text="0-default,1-hidden")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table="category"
    
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    slug=models.CharField(max_length=150)
    name=models.CharField(max_length=150)
    product_image=models.ImageField(upload_to="myimages")
    small_description=models.TextField(max_length=250) 
    status=models.BooleanField(default=False,help_text="0-default,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-hidden")
    quantity=models.IntegerField()
    description=models.TextField(max_length=500)
    original_price=models.IntegerField()
    selling_price=models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table="product"

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField()

    def __str__(self):
        return self.product

class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fname=models.CharField(max_length=100, null=False)
    lname=models.CharField(max_length=100, null=False)
    email=models.CharField(max_length=100, null=False)
    phone=models.CharField(max_length=100, null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=100, null=False)
    state=models.CharField(max_length=100, null=False)
    country=models.CharField(max_length=100, null=False)
    pincode=models.CharField(max_length=100, null=False)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=150, null=False)
    payment_id=models.CharField(max_length=250,null=True)
    orderstatuses = (
        ('pending','pending'),
        ('Out for shipping','Out for shipping'),
        ('Completed','Completed')
    )
    status=models.CharField(max_length=150,choices=orderstatuses, default='Pending')
    message=models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.order.id, self.order.tracking_no)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=100, null=False)
    state=models.CharField(max_length=100, null=False)
    country=models.CharField(max_length=100, null=False)
    pincode=models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username














class RegForm(UserCreationForm):
    class Meta:
        model=User
        fields=("first_name","last_name","email","username")
        widgets={
            "first_name" : forms.TextInput(attrs={'class':'form-control'}),
            "last_name" : forms.TextInput(attrs={'class':'form-control'}),
            "email" : forms.EmailInput(attrs={'class':'form-control'}),
            "username" : forms.TextInput(attrs={'class':'form-control'}),
        }

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control w-75 m-1 p-1'}))
    password=forms.CharField(max_length=35,widget=forms.PasswordInput(attrs={'class':'form-control w-75 m-1'}))
   
