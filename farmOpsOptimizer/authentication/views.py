from django.shortcuts import render, redirect
from authentication.forms import CustomUserCreationForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authentication:login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('login')