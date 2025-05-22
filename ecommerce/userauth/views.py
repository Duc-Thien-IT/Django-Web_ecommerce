from django.shortcuts import redirect, render
from userauth.form import UserRegisterForm, UserLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

User = settings.AUTH_USER_MODEL

def register_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
        
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Welcome {username}! Your account was created successfully")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    
    return render(request, "userauth/signup.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
        
    form = UserLoginForm()
    login_failed = False
    
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember_me = request.POST.get("remember_me")
            
            # Save remember_me choice to session
            if remember_me:
                request.session['remember_me'] = True
            else:
                request.session['remember_me'] = False
                
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                
                # Check if there's a next parameter in URL
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                return redirect("core:index")
            else:
                messages.error(request, "Invalid email or password")
                login_failed = True
        else:
            messages.error(request, "Please correct the errors below")
            login_failed = True
    
    context = {
        "form": form, 
        "login_failed": login_failed
    }
    return render(request, "userauth/signup.html", context)

def logout_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"Goodbye {username}! You have been logged out successfully")
    return redirect("core:index")