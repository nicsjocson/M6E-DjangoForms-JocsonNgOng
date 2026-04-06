from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dish, Account

def better_menu(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/better_list.html', {'dishes':dish_objects})

def add_menu(request):
    if(request.method=="POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.create(name=dishname, cook_time=cooktime, prep_time=preptime)
        return redirect('better_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('better_menu')

def update_dish(request, pk):
    if(request.method=="POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')
        Dish.objects.filter(pk=pk).update(cook_time=cooktime, prep_time=preptime)
        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        # for credentials checking
        account = Account.objects.filter(username=u, password=p).first()
        if account:
            return redirect('basic_list', pk=account.pk)
        else:
            messages.error(request, "Invalid login")
            
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        if Account.objects.filter(username=u).exists():
            messages.warning(request, "Account already exists")
        else:
            Account.objects.create(username=u, password=p)
            messages.success(request, "Account created successfully")
            return redirect('login')
            
    return render(request, 'signup.html')

def basic_list_view(request, pk):
    #logged-in account
    account = get_object_or_404(Account, pk=pk)
    
    #all the dishes so they display on the page
    dish_objects = Dish.objects.all() 
    
    context = {
        'account': account,
        'dishes': dish_objects
    }
    return render(request, 'basic_list.html', context)

def manage_account_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'manage_account.html', {'account': account})

def delete_account_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    return redirect('login')

def change_password_view(request, pk):
    account = get_object_or_404(Account, pk=pk)
    
    if request.method == 'POST':
        curr_p = request.POST.get('current_password')
        new_p = request.POST.get('new_password')
        confirm_p = request.POST.get('confirm_password')
        
        #requested getter method for the password
        if curr_p == account.getPassword() and new_p == confirm_p and new_p != "":
            account.password = new_p
            account.save()
            return redirect('manage_account', pk=pk)
        else:
            messages.error(request, "Invalid current password or new passwords do not match.")
            
    return render(request, 'change_password.html', {'account': account})