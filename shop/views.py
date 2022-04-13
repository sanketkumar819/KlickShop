from django.shortcuts import render, redirect
from .models import Customer, Product, OrderPlaced, Cart
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        param = {'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem}
        return render(request, 'shop/home.html',param)

class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_alredy = False
        if request.user.is_authenticated:
            item_alredy = Cart.objects.filter(Q(product=product.id)& Q(user=request.user)).exists()
        
        return render(request, 'shop/productdetail.html', {'product':product,'item_alredy':item_alredy})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.dicounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
        
            return render(request, 'shop/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
        else:
            return render(request,'shop/emptycart.html')

@login_required
def plus_cart(request):
   if request.method=="GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save() 
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.dicounted_price)
            amount += tempamount
            
                
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
         }
        return JsonResponse(data)

@login_required
def minus_cart(request):
   if request.method=="GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save() 
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.dicounted_price)
            amount += tempamount
           
                
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
         }
        return JsonResponse(data)
        
@login_required
def remove_cart(request):
   if request.method=="GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete() 
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.dicounted_price)
            amount += tempamount
            
                
        data = {
            
            'amount':amount,
            'totalamount': amount + shipping_amount
         }
        return JsonResponse(data)



def buy_now(request):
 return render(request, 'shop/buynow.html')

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request): 
        forms = CustomerProfileForm()
        return render(request, 'shop/profile.html',{'forms':forms,'active':'btn-primary'})
    
    def post(self, request):
        forms = CustomerProfileForm(request.POST)
        if forms.is_valid():
            usr = request.user
            name = forms.cleaned_data['name']
            locality = forms.cleaned_data['locality']
            city = forms.cleaned_data['city']
            state = forms.cleaned_data['state']
            zipcode = forms.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratualtions!! Profile updated Successfully ')
        return render(request, 'shop/profile.html',{'forms':forms,'active':'btn-primary'})

@login_required
def address(request):
    adds = Customer.objects.filter(user=request.user)
    return render(request, 'shop/address.html',{'adds':adds,'active':'btn-primary'})

@login_required
def orders(request):
    orp = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'shop/orders.html',{'orp':orp})


def mobile(request, data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif data=='Redmi' or data=='Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data=='below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price_lt=10000)
    elif data=='above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price_gt=10000)    
    return render(request, 'shop/mobile.html', {'mobiles':mobiles})


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm
        return render(request, 'shop/customerregistration.html', {'forms':form})
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratualtions!! Registered Successfully')
            form.save() 
        return render(request, 'shop/customerregistration.html', {'forms':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.dicounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
        
        
    return render(request, 'shop/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})


@login_required
def payment_done(request):
   
   user = request.user
   custid = request.GET.get('custid')
   customer = Customer.objects.get(id=custid)
   cart = Cart.objects.filter(user=user)
   for c in cart:
       OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save() 
       c.delete()
       
   return redirect('orders')