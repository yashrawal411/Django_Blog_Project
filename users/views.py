from multiprocessing import context
from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm ## can be removed now , no need !
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')

    else :
        form = UserRegisterForm()
    
    return render(request,'users/register.html',{'form' : form }) 


@login_required
def profile(request):

    if request.method == 'POST':
        ## middle argument has image data
        u_form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            messages.success(request,f'Yout Account has been updated !')
            return redirect('profile')
    else :

        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form , 'p_form':p_form}

    return render(request,'users/profile.html',context)
