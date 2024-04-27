from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record
# Create your views here.

def Home (request):
    messages.success(request,"Click On id to Update or Delete Record")
    records = Record.objects.all()
    #check to see if logging in
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(username=username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"You Haven LoggedIn Successfully")
            return redirect('home')
        else:
            messages.success(request,"Something Went Wrong...")
            return redirect('home')
    else:   
        return render(request,'core/home.html' ,{'records':records})




# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request,"You have been Logged Out....")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You Have Successfully Register Welcome...")
            return redirect('home')
    else:
        form = SignUpForm()        
        return render(request,'core/register.html',{'form':form})  
    return render(request,'core/register.html',{'form':form})    

def record_user(request,id):
    if request.user.is_authenticated:
        user_record = Record.objects.get(pk=id)
    return render(request,'core/record.html',{'user_record':user_record})    


def delete_record(request,id):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(pk=id)
        delete_it.delete()
        messages.success(request,'Record are Deleted Successfully....')
        return redirect('home')
    else:
        messages.success(request,'You must be LoggedIn...')
        return redirect('home')


def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Record Added...")
                return redirect('home')
        else:
            form = AddRecordForm()        
        return render(request,'core/add_record.html',{'form':form})
    else:
        messages.success(request,'You Must Be Logged In...')
        return redirect('home')    
    

def update_record(request,id):
    if request.user.is_authenticated:
        current_record = Record.objects.get(pk=id)
        form = AddRecordForm(request.POST or None,instance = current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Has Been Updated!')
            return redirect('home')
        return render(request,'core/update_record.html',{'form':form})
    else:
        messages.success(request,'You Must Be Logged In...')
        return redirect('home')  
      



