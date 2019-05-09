from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
from django.contrib.auth.management.commands import createsuperuser
from django.core.management.base import CommandError

class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        if self.UserModel.objects.filter(is_superuser=True).exists():
            raise CommandError("There is no room for two, go your way!")
        super().handle(*args, **options)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile_pic=models.ImageField(upload_to='images/',default='images/avatar.jpg')
    bio= HTMLField()
    more= HTMLField()
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    phone_number=models.IntegerField(null=True)
    email = models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=100,default='Rwanda',null=True)
    city = models.CharField(max_length=100,default='Kigali',null=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.first_name

    def delete_profile(self):
        self.delete()

    def update_bio(self,bio):
        self.bio=bio
        self.save()
   

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Category(models.Model):
    name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
    picture=models.ImageField(upload_to='images/', null=True)
    description = HTMLField()
    demo_video =  models.FileField(upload_to='videos/', null=True)
    district = models.CharField(max_length=100,null=True)
    sector = models.CharField(max_length=100,null=True)
    cell = models.CharField(max_length=100,null=True)
    street = models.CharField(max_length=100,null=True)
    building = models.CharField(max_length=100,null=True,blank = True)
    event_category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    duration = models.PositiveIntegerField(null=True)
    date_of_event = models.CharField(max_length=100,null=True)
    time= models.TimeField(null=True,verbose_name='Starting time for the event')

    post_date = models.DateTimeField(auto_now_add=True, null=True)
  
    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True)
    ticket_name = models.CharField(max_length=100,null=True)
    price = models.PositiveIntegerField(null=True)
    number_of_tickets = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.ticket_name

    def save_ticket(self):
        self.save()

    def delete_ticket(self):
        self.delete()

    @classmethod
    def get_comments_by_event(cls, id):
        tickets = Ticket.objects.filter(event__pk = id)
        return tickets

class Tpayment(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True)
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    number_of_tickets = models.PositiveIntegerField(null=True)
    ticket_category = models.ForeignKey(Ticket,on_delete=models.CASCADE, null=True)
    

class Payment(models.Model):
    tpayment = models.ForeignKey(Tpayment,on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event,on_delete=models.CASCADE, null=True)
    phonenumber=models.CharField(max_length=100,null=True)
    amount=models.CharField(max_length=100,null=True)
    number_of_tickets =  models.PositiveIntegerField(null=True)
    post_date = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.First_Name
    def save_payment(self):
        self.save()
