from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date
from django.shortcuts import get_object_or_404

#imports for API

from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics,mixins
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import authentication_classes,permission_classes


# Create your views here.
def home(request):
    return render(request,'design_home.html')

def ngo_signup(request):
    error=""
    if request.method=='POST':
        ngo_name=request.POST.get('ngo_name')
        emailid=request.POST.get('emailid')
        password=request.POST.get('password')
        contact=request.POST.get('contact')
        certificate=request.FILES.get('certificate')
        image=request.FILES.get('image')
        description=request.POST.get('description')
        registration_number=request.POST.get('registration_number')
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        address_line_1=request.POST.get('address_line_1')
        try:
            user= User.objects.create_user(
                username=emailid,
                password=password,
                is_active=True,
            )
            user.save()
            user_additional_data=NGOProfile.objects.create(
                user=user,
                contact=contact,
                certificate=certificate,
                country=country,
                state=state,
                city=city,
                pincode=pincode,
                address_line_1=address_line_1,
                registration_number=registration_number,
                ngo_name=ngo_name,
                image=image,
                description=description,
            )
            user_additional_data.save()
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'ngo_signup.html',d)


def user_signup(request):
    error=""
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        emailid=request.POST.get('emailid')
        password=request.POST.get('password')
        contact=request.POST.get('contact')
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        address_line_1=request.POST.get('address_line_1')

        try:
            user= User.objects.create_user(
                username=emailid,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            user.save()
            user_additional_data=UserProfile.objects.create(
                user=user,
                contact=contact,
                country=country,
                state=state,
                city=city,
                pincode=pincode,
                address_line_1=address_line_1,
            )
            user_additional_data.save()
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'user_signup.html',d)

def ngo_login(request):
    error=""
    if request.method == 'POST':
        email_id= request.POST['emailid']
        pass_word= request.POST['pwd']
        user = authenticate(username=email_id,password=pass_word)
        user_exists=False
        if user:
            user_exists=NGOProfile.objects.filter(user=user.id).exists()
        try:
            if user and user_exists:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error = "yes"
    d= {'error':error}
    return render(request,'ngo_login.html',d)

def user_login(request):
    error=""
    if request.method == 'POST':
        email_id= request.POST['emailid']
        pass_word= request.POST['pwd']
        user = authenticate(username=email_id,password=pass_word)
        user_exists=False
        if user:
            user_exists=UserProfile.objects.filter(user=user.id).exists()
        try:
            if user and user_exists:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error = "yes"
    d= {'error':error}
    return render(request,'user_login.html',d)

def adminlogin(request):
    error=""
    if request.method == 'POST':
        user_name= request.POST['uname']
        pass_word= request.POST['pwd']
        user = authenticate(username=user_name,password=pass_word)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error = "yes"
    d= {'error':error}
    return render(request,'adminlogin.html',d)

def adminhome(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    return render(request,'adminhome.html')

def Logout(request):
    logout(request)
    return redirect('home')

def ngo_profile(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None
    try:
        data = NGOProfile.objects.get(user=user)
    except NGOProfile.DoesNotExist:
        data = None
    d={'user':user,'data':data}
    return render(request,'ngo_profile.html',d)

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        user = None
    try:
        data = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        data = None
    d={'user':user,'data':data}
    return render(request,'user_profile.html',d)

def all_verified_ngos(request):
    if not request.user.is_authenticated:
        return redirect('home')
    ngos=NGOProfile.objects.filter(verfied=True)
    d={'ngos':ngos}
    return render(request,'all_verified_ngos.html',d)

def all_nonverified_ngos(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    ngos=NGOProfile.objects.filter(verfied=False)
    d={'ngos':ngos}
    return render(request,'all_nonverified_ngos.html',d)

def verify_ngo(request,pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    ngo = NGOProfile.objects.get(id=pid)
    ngo.verfied=True
    ngo.save()
    return redirect('all_nonverified_ngos')

def delete_ngo(request,pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    ngo=NGOProfile.objects.get(id=pid)
    user=User.objects.get(id=ngo.user.id)
    user.delete()
    return redirect('all_nonverified_ngos')

def view_users(request):
    if not request.user.is_staff:
        return redirect('adminlogin')
    users = UserProfile.objects.all()
    ngos = NGOProfile.objects.all()
    d={'users':users,'ngos':ngos}
    return render(request,'view_users.html',d)

def delete_ngo_2(request,pid):
    if not request.user.is_staff:
        return redirect('adminlogin')
    ngo=NGOProfile.objects.get(id=pid)
    user=User.objects.get(id=ngo.user.id)
    user.delete()
    return redirect('view_users')

def changepassworduser(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('user_login')
    if request.method=='POST':
        o=request.POST.get('old')
        n=request.POST.get('new')
        c=request.POST.get('confirm')
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'changepassworduser.html',d)

def changepasswordngo(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    if request.method=='POST':
        o=request.POST.get('old')
        n=request.POST.get('new')
        c=request.POST.get('confirm')
        if c==n:
            u=User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d={'error':error}
    return render(request,'changepasswordngo.html',d)

def ngo_add_requirements(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    error=""
    if request.method=='POST':
        requirement=request.POST.get('requirement')
        quantity=request.POST.get('quantity')
        message=request.POST.get('message')
        n= NGOProfile.objects.get(user=request.user.id)
        try:
            user= NgoRequirements.objects.create(ngo=n,requirement=requirement,quantity=quantity,message=message)
            user.save()
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'ngo_add_requirements.html',d)

def ngo_delete_requirement(request,pid):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    ngo_req=NgoRequirements.objects.get(id=pid)
    reciept=Reciept.objects.filter(ngo_add_requirement=ngo_req.requirement)
    ngo_req.delete()
    reciept.delete()
    return redirect('ngo_self_requirements')

def ngo_edit_requirement(request,pid):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    error=""
    ngo_req=NgoRequirements.objects.get(id=pid)
    ngo=NGOProfile.objects.filter(id=ngo_req.ngo.id).first()
    if request.method=="GET":
        d={'ngo_req':ngo_req,'ngo_details':ngo,'error':error}
        return render(request,"ngo_edit_requirement.html",d)
    elif request.method=="POST":
        quantity=request.POST.get('quantity')
        message=request.POST.get('message')
        try:
            ngo_req.quantity=quantity
            ngo_req.message=message
            ngo_req.save()
            error="no"
        except:
            error="yes"
        d={'ngo_req':ngo_req,'ngo_details':ngo,'error':error}
        return render(request,"ngo_edit_requirement.html",d)

def user_ngo_view(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    ngos=NGOProfile.objects.filter(verfied=True)
    return render(request,'user_ngo_view.html',{"ngos":ngos})


def user_ngo_information(request,ngo_pk):
    if not request.user.is_authenticated:
        return redirect('user_login')

    ngo=NGOProfile.objects.get(id=ngo_pk)
    ngo_req=NgoRequirements.objects.filter(ngo=ngo)
    user=User.objects.get(username=ngo)
    ngo_details=NGOProfile.objects.get(user=user)
    error=""
    if request.method=="POST":
        arr=[]
        arr2=[]
        for i in ngo_req:
            arr.append(i.id)
            a=request.POST.get("donation"+str(i.id))
            if a=="":
                a=0
            else:
                a=int(a)
            if int(i.quantity)<=a:
                i.quantity=0
            else:
                i.quantity=int(i.quantity)-a
            i.save()
            arr2.append(int(a))

        for i in range(len(arr2)):
            if arr2[i]!=0:
                requirement=NgoRequirements.objects.get(id=arr[i]).requirement
                donated_items=arr2[i]
                user=User.objects.get(id=request.user.id)
                user_profile=UserProfile.objects.get(user=user)
                Reciept.objects.create(
                    ngo=ngo,
                    user=user_profile,
                    ngo_add_requirement=requirement,
                    donated_items=donated_items
                    ).save()
        error="no"


    data={"ngo_req":ngo_req,"ngo_details":ngo_details,'error':error}
    return render(request,"user_ngo_information.html",data)

def user_donator_list(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    a=User.objects.get(id=request.user.id)
    b=NGOProfile.objects.get(user=a)
    c=Reciept.objects.filter(ngo=b)
    d={'users':c}

    return render(request,'user_donator_list.html',d)

def ngo_self_requirements(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    ngo=User.objects.get(id=request.user.id)
    ngo_data=NGOProfile.objects.get(user=ngo)
    ngo_req=NgoRequirements.objects.filter(ngo=ngo_data)
    d={'ngo_req':ngo_req,'ngo_details':ngo_data}
    return render(request,"ngo_self_requirements.html",d)


# API views#########################################################################################################################################################

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def api_donor_list(request):
    if request.method=="GET":
        users=User.objects.all()
        donor_users=User.objects.none()
        user_profile=[]
        for a in users:
            if a.first_name!="" and a.last_name!="":
                donor_users |=User.objects.filter(pk=a.pk)
                user_profile.append(UserProfile.objects.filter(user=a).first())
        serializer=UserProfileSerializer(donor_users,many=True)
        data=[]
        i=0
        for a in serializer.data:
            d={}
            d.update({'id':a['id']})
            d.update({'username':a['username']})
            d.update({'first_name':a['first_name']})
            d.update({'last_name':a['last_name']})
            d.update({'password':a['password']})
            d.update({'contact':user_profile[i].contact})
            d.update({'address_line_1':user_profile[i].address_line_1})
            d.update({'city':user_profile[i].city})
            d.update({'state':user_profile[i].state})
            d.update({'country':user_profile[i].country})
            d.update({'pincode':user_profile[i].pincode})
            data.append(d)
            i=i+1
        return Response(data)

    elif request.method=="POST":
        serializer=UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.newsave()
            token=Token.objects.create(user=user)
            user_profile=UserProfile.objects.filter(user=user).first()
            data={
                'id':user.id,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'password':user.password,
                'contact':user_profile.contact,
                'address_line_1':user_profile.address_line_1,
                'city':user_profile.city,
                'state':user_profile.state,
                'country':user_profile.country,
                'pincode':user_profile.pincode,
                'token':token.key
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def api_donor_detail(request,pk):
    try:
        user=User.objects.get(pk=pk)
        user_profile=UserProfile.objects.filter(user=user).first()
        user_donations=Reciept.objects.filter(user=user_profile)
        token,_=Token.objects.get_or_create(user=user)

    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        serializer=UserProfileSerializer(user)
        data={}
        if user_profile!=None:
            donations=[]
            if user_donations!=None:
                for d in user_donations:
                    donation={
                        'id':d.id,
                        'ngo':d.ngo.ngo_name,
                        'ngo_email':d.ngo.user.username,
                        'requirement':d.ngo_add_requirement,
                        'donated_items':d.donated_items,
                    }
                    donations.append(donation)
            data={
                'id':serializer.data['id'],
                'username':serializer.data['username'],
                'first_name':serializer.data['first_name'],
                'last_name':serializer.data['last_name'],
                'password':serializer.data['password'],
                'contact':user_profile.contact,
                'address_line_1':user_profile.address_line_1,
                'city':user_profile.city,
                'state':user_profile.state,
                'country':user_profile.country,
                'pincode':user_profile.pincode,
                'donations':donations,
                'token':token.key
            }
            return Response(data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method=="DELETE":
        if user_profile!=None:
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DonorLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        user_profile=UserProfile.objects.filter(user=user).first()
        if user is not None and user_profile is not None:
            token,_ =Token.objects.get_or_create(user=user)
            donations=Reciept.objects.filter(user=user_profile)
            donations_data=[]
            if (donations!=None):
                for donation in donations:
                    d={
                        'id':donation.id,
                        'ngo_email':donation.ngo.user.username,
                        'ngo':donation.ngo.ngo_name,
                        'requirement':donation.ngo_add_requirement,
                        'donated_items':donation.donated_items,
                    }
                    donations_data.append(d)
            login(request, user)
            data={
                'id':user.id,
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'password':user.password,
                'contact':user_profile.contact,
                'address_line_1':user_profile.address_line_1,
                'city':user_profile.city,
                'state':user_profile.state,
                'country':user_profile.country,
                'pincode':user_profile.pincode,
                'donations':donations_data,
                'token':token.key
            }
            return Response(data)
        else:
            data = {"Message": "There was error authenticating"}
            return JsonResponse(data)

class NGOLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        user_profile=NGOProfile.objects.filter(user=user).first()
        if user is not None and user_profile is not None:
            token,_ =Token.objects.get_or_create(user=user)
            requirements=NgoRequirements.objects.filter(ngo=user_profile)
            requirements_data=[]
            if (requirements!=None):
                for requirement in requirements:
                    d={
                        'id':requirement.id,
                        'requirement':requirement.requirement,
                        'quantity':requirement.quantity,
                        'message':requirement.message
                    }
                    requirements_data.append(d)
            login(request, user)
            data={
                'id':user.id,
                'registration_number':user_profile.registration_number,
                'ngo_name':user_profile.ngo_name,
                'username':user.username,
                'password':user.password,
                'contact':user_profile.contact,
                'certificate':user_profile.certificate.url,
                'image':user_profile.image.url,
                'address_line_1':user_profile.address_line_1,
                'city':user_profile.city,
                'state':user_profile.state,
                'country':user_profile.country,
                'pincode':user_profile.pincode,
                'requirements':requirements_data,
                'token':token.key
            }
            return Response(data)
        else:
            data = {"Message": "There was error authenticating"}
            return JsonResponse(data)

class Verified_NGO_list(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NGOProfileSerializer

    def get(self,request,*args,**kwargs):
        ngo_profiles=NGOProfile.objects.filter(verfied=True)
        if ngo_profiles is not None:
            data=[]
            for ngo_profile in ngo_profiles:
                token,_ =Token.objects.get_or_create(user=ngo_profile.user)
                requirements=NgoRequirements.objects.filter(ngo=ngo_profile)
                requirements_data=[]
                if (requirements!=None):
                    for requirement in requirements:
                        d={
                            'id':requirement.id,
                            'requirement':requirement.requirement,
                            'quantity':requirement.quantity,
                            'message':requirement.message
                        }
                        requirements_data.append(d)
                d={
                    'id':ngo_profile.user.id,
                    'registration_number':ngo_profile.registration_number,
                    'ngo_name':ngo_profile.ngo_name,
                    'username':ngo_profile.user.username,
                    'password':ngo_profile.user.password,
                    'contact':ngo_profile.contact,
                    'certificate':ngo_profile.certificate.url,
                    'image':ngo_profile.image.url,
                    'address_line_1':ngo_profile.address_line_1,
                    'city':ngo_profile.city,
                    'state':ngo_profile.state,
                    'country':ngo_profile.country,
                    'pincode':ngo_profile.pincode,
                    'requirements':requirements_data,
                    'token':token.key
                }
                data.append(d)
            return Response(data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Ngo_Donor_list(request,pk):
    if request.method=="GET":
        user=User.objects.get(pk=pk)
        ngo=NGOProfile.objects.filter(user=user).first()
        reciepts=Reciept.objects.filter(ngo=ngo)
        serializer=RecieptsSerializer(reciepts,many=True)
        return Response(serializer.data)


class Ngo_Requirement_list(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        user=User.objects.get(pk=pk)
        ngo_profile=NGOProfile.objects.filter(user=user).first()
        requirements=NgoRequirements.objects.filter(ngo=ngo_profile)
        serializer=RequirementsSerializer(requirements,many=True)
        return Response(serializer.data)

    def post(self,request,pk):
        user=User.objects.get(pk=pk)
        ngo_profile=NGOProfile.objects.filter(user=user).first()
        requirement=NgoRequirements.objects.create(ngo=ngo_profile,
                                                requirement=request.data.get("requirement"),
                                                quantity=request.data.get("quantity"),
                                                message=request.data.get("message"))
        requirement.save()
        serializer=RequirementsSerializer(requirement)
        return Response(serializer.data)


class Ngo_Requirement_detail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk,r_pk):
        requirement=NgoRequirements.objects.get(pk=r_pk)
        serializer=RequirementsSerializer(requirement)
        return Response(serializer.data)

    def delete(self, request,pk,r_pk):
        requirement=NgoRequirements.objects.get(pk=r_pk)
        if requirement is not None:
            requirement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request,pk,r_pk):
        user=User.objects.get(pk=pk)
        ngo_profile=NGOProfile.objects.filter(user=user).first()
        requirement=NgoRequirements.objects.get(pk=r_pk)
        data={
            'requirement':request.data['requirement'],
            'quantity':request.data['quantity'],
            'message':request.data['message'],
            'ngo':ngo_profile.id
        }
        serializer=RequirementsSerializer(requirement,data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class api_ngo_list(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class=NGOProfileSerializer
    queryset = User.objects.all()
    def get(self,request):
        users=User.objects.all()
        ngo_users=User.objects.none()
        ngo_profile=[]
        for a in users:
            if a.first_name=="" and a.last_name=="" and a.email=="":
                ngo_users |=User.objects.filter(pk=a.pk)
                ngo_profile.append(NGOProfile.objects.filter(user=a).first())
        serializer=UserProfileSerializer(ngo_users,many=True)
        data=[]
        i=0
        for a in serializer.data:
            requirements=NgoRequirements.objects.filter(ngo=ngo_profile[i])
            requirements_data=[]
            if (requirements!=None):
                for requirement in requirements:
                    d={
                        'id':requirement.id,
                        'requirement':requirement.requirement,
                        'quantity':requirement.quantity,
                        'message':requirement.message
                    }
                    requirements_data.append(d)
            d={
                'id':a['id'],
                'verified':ngo_profile[i].verfied,
                'ngo_name':ngo_profile[i].ngo_name,
                'username':a['username'],
                'password':a['password'],
                'registration_number':ngo_profile[i].registration_number,
                'certificate':ngo_profile[i].certificate.url,
                'image':ngo_profile[i].image.url,
                'contact':ngo_profile[i].contact,
                'description':ngo_profile[i].description,
                'requirements':requirements_data,
                'address_line_1':ngo_profile[i].address_line_1,
                'city':ngo_profile[i].city,
                'state':ngo_profile[i].state,
                'country':ngo_profile[i].country,
                'pincode':ngo_profile[i].pincode
            }
            data.append(d)
            i=i+1
        return Response(data)

    def post(self,request,*args,**kwargs):
        serializer=NGOProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.newsave()
            ngo_profile=NGOProfile.objects.filter(user=user).first()
            token = Token.objects.create(user=user)
            data={
                'id':user.id,
                'verified':ngo_profile.verfied,
                'ngo_name':ngo_profile.ngo_name,
                'username':user.username,
                'password':user.password,
                'registration_number':ngo_profile.registration_number,
                'certificate':ngo_profile.certificate.url,
                'image':ngo_profile.image.url,
                'contact':ngo_profile.contact,
                'description':ngo_profile.description,
                'address_line_1':ngo_profile.address_line_1,
                'city':ngo_profile.city,
                'state':ngo_profile.state,
                'country':ngo_profile.country,
                'pincode':ngo_profile.pincode,
                'token':token.key
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class api_ngo_detail(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class=NGOProfileSerializer
    queryset = User.objects.all()

    def get(self,request,pk):
        user=User.objects.get(pk=pk)
        ngo_profile=NGOProfile.objects.filter(user=user).first()
        requirements=NgoRequirements.objects.filter(ngo=ngo_profile)
        serializer=NGOProfileSerializer(user)
        requirements_data=[]
        if (requirements!=None):
            for requirement in requirements:
                d={
                    'id':requirement.id,
                    'requirement':requirement.requirement,
                    'quantity':requirement.quantity,
                    'message':requirement.message
                }
                requirements_data.append(d)
        data={
            'id':serializer.data['id'],
            'verified':ngo_profile.verfied,
            'ngo_name':ngo_profile.ngo_name,
            'username':serializer.data['username'],
            'password':serializer.data['password'],
            'registration_number':ngo_profile.registration_number,
            'certificate':ngo_profile.certificate.url,
            'image':ngo_profile.image.url,
            'contact':ngo_profile.contact,
            'description':ngo_profile.description,
            'requirements':requirements_data,
            'address_line_1':ngo_profile.address_line_1,
            'city':ngo_profile.city,
            'state':ngo_profile.state,
            'country':ngo_profile.country,
            'pincode':ngo_profile.pincode
        }
        return Response(data)


    def delete(self, request,pk):
        user=User.objects.get(pk=pk)
        if user is not None:
            user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class api_donor_donate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk,n_pk):
        donor=User.objects.get(pk=pk)
        ngo=User.objects.get(pk=n_pk)
        donor_profile=UserProfile.objects.filter(user=donor).first()
        ngo_profile=NGOProfile.objects.filter(user=ngo).first()
        reciepts=Reciept.objects.filter(ngo=ngo_profile,user=donor_profile)
        serializer=RecieptsSerializer(reciepts,many=True)
        return Response(serializer.data)

    def post(self,request,pk,n_pk):
        donor=User.objects.get(pk=pk)
        ngo=User.objects.get(pk=n_pk)
        donor_profile=UserProfile.objects.filter(user=donor).first()
        ngo_profile=NGOProfile.objects.filter(user=ngo).first()
        data={
            'ngo_add_requirement':request.data['ngo_add_requirement'],
            'donated_items':request.data['donated_items'],
            'ngo':ngo_profile.id,
            'user':donor_profile.id
        }
        requirement=NgoRequirements.objects.filter(ngo=ngo_profile,requirement=request.data['ngo_add_requirement']).first()
        if requirement is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        requirement.quantity = 0 if (requirement.quantity<request.data['donated_items']) else (requirement.quantity-request.data['donated_items'])
        requirement.save()
        serializer=RecieptsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

class api_donor_donation_detail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk,n_pk,r_pk):
        donor=User.objects.get(pk=pk)
        ngo=User.objects.get(pk=n_pk)
        donor_profile=UserProfile.objects.filter(user=donor).first()
        ngo_profile=NGOProfile.objects.filter(user=ngo).first()
        reciept=Reciept.objects.filter(ngo=ngo_profile,user=donor_profile,pk=r_pk).first()
        serializer=RecieptsSerializer(reciept)
        return Response(serializer.data)

    def delete(self, request,pk,n_pk,r_pk):
        reciept=Reciept.objects.get(pk=r_pk)
        if reciept is not None:
            reciept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
