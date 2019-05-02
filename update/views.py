from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,Event,Ticket,Category,Tpayment
from .forms import ProfileForm,EventForm,TicketForm,TpaymentForm
import datetime as dt
# Create your views here.


def welcome(request):
    return render(request, 'welcome.html',)


def home(request):
    date = dt.date.today()
    user = request.user
    event = Event.objects.all()
    return render(request, 'home.html',{"date": date,"user":user,"event":event})

@login_required(login_url='/accounts/login/')
def profile(request,edit):
    current_user = request.user
    profile=Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.bio=form.cleaned_data['bio']
            profile.more=form.cleaned_data['more']
            profile.profile_pic = form.cleaned_data['profile_pic']
            profile.email = form.cleaned_data['email']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.user=current_user
            
            profile.save()
            return redirect(home)
    else:
        form = ProfileForm()
    return render(request, 'profile_form.html', {"form": form,'user':current_user})

def myProfile(request,id):
    user = User.objects.get(id = id)
    profiles = Profile.objects.get(user = user)
    event = Event.objects.filter(user = user).all()

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.save(commit=False)
            price.user = current_user
            price.save()

            return redirect(home)

    else:
        form = TicketForm()
    
    return render(request,'my_profile.html',{"form":form,"profiles":profiles,"user":user,"event":event})

def price(request,id):
    user = request.user
    event = Event.objects.get(id = id)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            price = form.save(commit=False)
            price.user = user
            price.event=event
            price.save()

            return redirect(home)

    else:
        form = TicketForm()
    
    return render(request,'price.html',{"form":form,"user":user,"event":event})

@login_required(login_url='/accounts/login/')
def event(request):
    current_user = request.user
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = current_user
            event.save()

            return redirect(home)

    else:
        form = EventForm()
    return render(request, 'event.html', {"form": form})

def organiser(request):
    user = User.objects.all()
    return render(request, 'organiser.html',{"user":user})

def info(request,id):
    post = Event.objects.get(id=id)
    ticket = Ticket.objects.filter(event=post)

  
    return render(request, 'info.html', {'post':post,'ticket':ticket})


def category(request,category_id):
    
    event_category = Category.objects.get(id = category_id)
    event = Event.objects.filter(event_category = event_category.id)
    
    return render(request,'category.html',{'category':category,'event':event})

def ticket(request,id):
    current_user = request.user
    post = Event.objects.get(id=id)
    ticket = Ticket.objects.filter(event=post)

    if request.method == 'POST':
        form = TpaymentForm(request.POST, request.FILES)
        if form.is_valid():
            pay = form.save(commit=False)
            pay.user = current_user
            pay.event=post
            pay.save()

            return redirect(home)

    else:
        form = TpaymentForm()
  
    return render(request, 'ticket.html', {"form": form,"current_user":current_user,"post":post})