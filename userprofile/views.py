from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import UserProfile

# Create your views here.

def vendor_detail(request,pk):
    user = User.objects.get(pk=pk)
    
    return render(request,'userprofile/vendor_detail.html',{'user':user})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request,user)
            #create a user profile
            userprofile = UserProfile.objects.create(user=user)
            
            return redirect('home')
    else:
            form = UserCreationForm()
    return render(request,'userprofile/signup.html',{'form':form})

def myaccount(request):
    return render(request,'userprofile/myaccount.html')