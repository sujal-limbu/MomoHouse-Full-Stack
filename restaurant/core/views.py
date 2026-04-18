from django.shortcuts import render,redirect
from .models import Contact,Category,Momo
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions  import ValidationError
import qrcode
import re
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.

def index(request):
    date = datetime.now()

    category = Category.objects.all()
    cateid = request.GET.get("category")

    if cateid == 'full':
        momo = Momo.objects.all()
    elif cateid:
        momo = Momo.objects.filter(category=cateid)
    else:
        momo = Momo.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(name=name,phone=phone,email=email,message=message)
        return redirect("index")
    context = {
        'category':category,
        'momo':momo
    }
    return render(request,'core/index.html',context)

@login_required(login_url='login')
def menu(request):
    qr = qrcode.make("http://127.0.0.1:8000/menu")
    qr.save("core/static/images/menu.png")
    category = Category.objects.all()
    return render(request,'core/menu.html',{'category':category })

@login_required(login_url='login')
def about(request):
    return render(request,'core/about.html')

def contact(request):
    return render(request,'core/contact.html')

def services(request):
    return render(request,'core/services.html' )

def testemonial(request):
    return render(request,'core/testemonial.html')

def privacy(request):
    return render(request,'core/privacy.html')

def term(request):
    return render(request,'core/term.html')

'''
======================
Authentication
======================
'''
def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if (password == password1):

            error = []

            if User.objects.filter(username=username).exists():
                error.append("User already exist")
                
            if User.objects.filter(email=email).exists():
                error.append("Email already exist")
                
            if not re.search(r'[A-Z]',password):
                error.append('password must have at least one uppercase')
                
            if not re.search(r'\d',password):
                error.append('password must have at least one digit')
                
            if not re.search(r'\W',password):
                error.append('password must have at least special characteristic')
            
            try:
                validate_password(password)

                if not error:
                    User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                    messages.success(request,"register successfully")
                    return redirect('register')
                else:
                    for i in error:
                        messages.error(request,i)
                    return redirect('register')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
        else:
            messages.error(request,"Password and Confirm doesnot match")
            return redirect('register')


    return render(request,'accounts/register.html')

def log_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'user not registered')
            return redirect('login')


        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)

            if remember_me:
                request.session.set_expiry(1800)
            else:
                request.session.set_expiry(0)

            next = request.POST.get('next')
            return redirect(next if next else index)
        else:
            messages.error(request,'password_invalid')
            return redirect('login')
    next = request.GET.get('next','')
    return render(request, 'accounts/login.html',{'next':next})
    
def log_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user,data = request.POST)
        if form.is_valid():
             form.save()
             return redirect('login')
    return render(request,'accounts/change_password.html',{'form':form})
        
    
   


