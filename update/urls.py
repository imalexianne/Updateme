from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.welcome,name = 'welcome'),
    url(r'^home/',views.home,name = 'home'),
    url(r'^profile/(\d+)',views.profile,name ='profile'),
    url(r'^myProfile/(\d+)', views.myProfile, name='myProfile'),
    url(r'^event/', views.event, name='event'),  
    url(r'^info/(\d+)', views.info, name='info'),  
    url(r'^organiser/', views.organiser, name='organiser'),    
    url(r'^category/(\d+)',views.category,name ='category'),   
    url(r'^ticket/(\d+)',views.ticket,name ='ticket'),   
    url(r'^price/(\d+)',views.price,name ='price'),
    url(r'^payment/(\d+)',views.payments,name ='payment'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
