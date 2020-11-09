"""NGO_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NGO_App.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('ngo_signup/',ngo_signup,name='ngo_signup'),
    path('user_signup/',user_signup,name='user_signup'),
    path('ngo_login/',ngo_login,name='ngo_login'),
    path('user_login/',user_login,name='user_login'),
    path('adminlogin/',adminlogin,name="adminlogin"),
    path('ngo_profile/',ngo_profile,name='ngo_profile'),
    path('user_profile/',user_profile,name='user_profile'),
    path('adminhome/',adminhome,name="adminhome"),
    path('logout/',Logout,name="logout"),
    path('all_verified_ngos/',all_verified_ngos,name='all_verified_ngos'),
    path('all_nonverified_ngos/',all_nonverified_ngos,name='all_nonverified_ngos'),
    path('verify_ngo/<int:pid>/',verify_ngo,name="verify_ngo"),
    path('delete_ngo/<int:pid>/',delete_ngo,name="delete_ngo"),
    path('view_users',view_users,name="view_users"),
    path('delete_ngo_2/<int:pid>/',delete_ngo_2,name="delete_ngo_2"),
    path('changepassworduser/',changepassworduser,name="changepassworduser"),
    path('changepasswordngo/',changepasswordngo,name="changepasswordngo"),
    path('ngo_add_requirements/',ngo_add_requirements,name="ngo_add_requirements"),
    path('ngo_delete_requirement/<int:pid>/',ngo_delete_requirement,name="ngo_delete_requirement"),
    path('ngo_edit_requirement/<int:pid>/',ngo_edit_requirement,name="ngo_edit_requirement"),
    path('user_ngo_view/',user_ngo_view,name="user_ngo_view"),
    path('user_ngo_information/<int:ngo_pk>/',user_ngo_information,name="user_ngo_information"),
    path('user_donator_list/',user_donator_list,name="user_donator_list"),
    path('ngo_self_requirements/',ngo_self_requirements,name="ngo_self_requirements"),

    #API URLs

    path('api_donor_list/',api_donor_list,name="api_donor_list"),#Gives the donors list only to admin {get and post}
    path('api_donor_detail/<int:pk>',api_donor_detail,name="api_donor_detail"),#Gives individual donor detail only to admin {get and delete}
    path('api_donor_login/',DonorLogin.as_view(),name="api_donor_login"),#allows donor to log into his account {post}
    path('api_ngo_login/',NGOLogin.as_view(),name="api_ngo_login"),#allows ngo to log into the account {post}
    path('verified_ngo_list/',Verified_NGO_list.as_view(),name="verified_ngo_list"),#gives list of verified ngo's to the person logged in {get}
    path('api_ngo_donor_list/<int:pk>',Ngo_Donor_list,name="api_ngo_donor_list"),#gives list of donors who made donation to a particular ngo of id=pk {get}
    path('api_ngo_requirement_list/<int:pk>',Ngo_Requirement_list.as_view(),name="api_ngo_requirement_list"),#gives the requirement list of ngo's of id=pk {get,post}
    path('api_ngo_requirement_detail/<int:pk>/<int:r_pk>',Ngo_Requirement_detail.as_view(),name="api_ngo_requirement_detail"),#gives the requirement details of particular
    #requirement of ngo's of id=pk and requrement id= r_pk {get,put,delete}
    path('api_ngo_list/',api_ngo_list.as_view(),name="api_ngo_list"),#gives the list of ngo's only to the admin {get and post}
    path('api_ngo_detail/<int:pk>',api_ngo_detail.as_view(),name="api_ngo_detail"),#gives the details of ngo only to the admin {get and delete}
    path('api_donor_donate/<int:pk>/<int:n_pk>',api_donor_donate.as_view(),name="api_donor_donate"),#gives list of donations made by donor of id=pk to ngo of id=n_pk
    path('api_donor_donation_detail/<int:pk>/<int:n_pk>/<int:r_pk>',api_donor_donation_detail.as_view(),name="api_donor_donation_detail"),#gives detail of donation id=r_pk
    #by donor id=pk to ngo id=n_pk
]

if settings.DEBUG:
    urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
