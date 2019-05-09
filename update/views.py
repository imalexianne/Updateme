from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,Event,Ticket,Category,Tpayment,Payment
from .forms import ProfileForm,EventForm,TicketForm,TpaymentForm,PaymentForm
import datetime as dt
import requests
import random
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
    ticket = Ticket.objects.filter(event = event.id).first()
    # print(event)
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
    ticket = Ticket.objects.filter(event=post).all()
    return render(request, 'info.html', {'post':post,'ticket':ticket})


def category(request,category_id):
    
    event_category = Category.objects.get(id = category_id)
    event = Event.objects.filter(event_category = event_category.id)
    
    return render(request,'category.html',{'category':category,'event':event})

def ticket(request,id):
    current_user = request.user
    copyname=request.POST.get('filter_by_category')
    post = Event.objects.get(id=id)
    ticket = Ticket.objects.filter(event=post)
    
    cat = ''
    print(copyname)
    
    if request.method == 'POST':
        form = TpaymentForm(request.POST, request.FILES)
        ticket_cat = Ticket.objects.get(id=int(copyname))
        if form.is_valid():
            # cat = form.cleaned_data.get('filter_by_category')
            # print(form)
            num = ticket_cat.number_of_tickets-1
            print(num)
            pay = form.save(commit=False)
            pay.user = current_user
            pay.event=post
            pay.ticket_category=ticket_cat
            print(pay.ticket_category)
            pay.save()

            
            return redirect('payment', id=pay.id)

    else:
        form = TpaymentForm()
        # form.fields['ticket_category'].initial = ticket
  
    return render(request, 'ticket.html', {"form": form,"current_user":current_user,"post":post,"ticket":ticket})


def payments(request,id):
    current_user = request.user
    data = {}
    hashed = random.randint(0,1000000)
    tpayment = Tpayment.objects.filter(id=id).first()
    ticket=Ticket.objects.filter(id = tpayment.ticket_category_id).first()
    price = ticket.price * tpayment.number_of_tickets
    remain = ticket.number_of_tickets - tpayment.number_of_tickets
    print(ticket.price)
    if request.method == 'POST':
        form = PaymentForm(request.POST,request.FILES)
        if form.is_valid():
            pay = form.save(commit=False)
            data['amount'] = str(price)
            data['phonenumber'] = pay.phonenumber
            data['clienttime'] = '1556616823718'
            data['action'] = "deposit"
            data['appToken'] = "9563d7e60dc40e0315bc"
            data['hash'] = hashed
            pay.user = current_user

            print(data)
            pay.save()
            payload = data
            url = "https://uplus.rw/bridge/"
            requests.post(url, data=payload)
            return redirect("home")
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {"form": form,"price":price,"tpayment":tpayment,"ticket":ticket,"remain":remain})
