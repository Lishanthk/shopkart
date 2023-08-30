import json
from django.http import JsonResponse
from django.shortcuts import redirect, render  
from shop.form import CustomUserForm
from . models import*
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

def home(request):
    products=product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            
            product_status=product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,products_id=product_id):
                    return JsonResponse({'status':'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,products_id=product_id,products_qty=product_qty)
                        return JsonResponse({'status':'Product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available'}, status=200)
                
                
        else:
            return JsonResponse({'status':'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    

def collections(request):
    dict_cat = {
        'catagory':Catagory.objects.filter(status=0)}
    return render(request,"shop/collections.html",dict_cat)


def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=product.objects.filter(Catagory__name=name)
        return render(request,"shop/pindex.html",{"products":products,"catagory_name":name})
    else:messages.warning(request,"No Such Catogory Found")
    return redirect('collections')
        
                                        
def prodetails(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products=product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/prodetails.html",{"products":products})
        else:
            messages.error(request,"NO Such product Found")
            return redirect('collections')
    else:
        messages.error(request,"NO Such Catagory Found")
        return redirect('collections')
    

    
   
    
    
  
    





def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect('/')
    


def login_page(request):
    if request.method=='POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid User Name or Password")
            return redirect("/login")
    return render(request,"shop/login.html")


def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,'Registration Success You can Login Now..!')
          return redirect("/login")
    return render(request,"shop/register.html",{'form':form})



def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,"shop/cart.html",{'cart':cart})
    

def remove_cart(request,id):
    cartitem=Cart.objects.get(id=id)
    cartitem.delete()
    return redirect('/cart')
    
