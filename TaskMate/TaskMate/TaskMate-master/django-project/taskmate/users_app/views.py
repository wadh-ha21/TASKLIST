from django.shortcuts import render, redirect
from .forms import CustomRegisterForm
from django.contrib import messages
from django.contrib.auth import logout



def register(request):
   if request.method=="POST":
     register_form = CustomRegisterForm(request.POST)
     if register_form.is_valid():
       register_form.save()
       messages.success(request, ('User account created successfully! Login to get started'))
       return redirect('register')
   else:
      register_form =CustomRegisterForm()
   return render(request, 'register.html', {'register_form': register_form}) 



def custom_logout(request):
   logout(request)
   return render(request,'logout.html')




