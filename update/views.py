from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import datetime as dt
# Create your views here.
def home(request):
    date = dt.date.today()
    return render(request, 'home.html',{"date": date,})