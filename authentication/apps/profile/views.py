from django.shortcuts import render, redirect
from .models import User

def profile(request):
    user_email = request.COOKIES.get('registered_email') 
    if user_email:
        try:
            user = User.objects.get(email=user_email) 
            return render(request, 'Profile.html', {'user': user})
        except User.DoesNotExist:
            return redirect('/login')  
    else:
        return redirect('/login') 
