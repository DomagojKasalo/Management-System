from .models import Uloge
from django.shortcuts import redirect

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.uloge.uloga == 'admin':
            return function(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrap

def profesor_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.uloge.uloga == 'profesor':
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

def student_required(function):
    def wrap(*args, **kwargs):
        if args[0].user.uloge.uloga == 'student':
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

