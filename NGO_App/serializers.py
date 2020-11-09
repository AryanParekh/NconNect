from rest_framework import serializers
from .models import *

class NGOProfileSerializer(serializers.ModelSerializer):

    def newsave(self):
        user=User(username=self.validated_data['username'])
        password=self.validated_data['password']
        user.set_password(password)
        user.save()
        user_profile=NGOProfile.objects.create(user=user,
                                            registration_number=self.validated_data['registration_number'],
                                            ngo_name=self.validated_data['ngo_name'],
                                            certificate=self.validated_data.get('certificate'),
                                            image=self.validated_data.get('image'),
                                            description=self.validated_data['description'],
                                            contact=self.validated_data['contact'],
                                            country=self.validated_data['country'],
                                            state=self.validated_data['state'],
                                            city=self.validated_data['city'],
                                            pincode=self.validated_data['pincode'],
                                            verfied=False,
                                            address_line_1=self.validated_data['address_line_1'])
        user_profile.save()
        return user


    registration_number=serializers.CharField(max_length=10,default='')
    ngo_name=serializers.CharField(max_length=50,default='')
    certificate=serializers.ImageField(default='')
    image=serializers.ImageField(default='')
    description=serializers.CharField(max_length=1000,default='')
    contact = serializers.CharField(max_length=10,default='')
    country=serializers.CharField(max_length=50,default='')
    state=serializers.CharField(max_length=50,default='')
    city=serializers.CharField(max_length=50,default='')
    pincode=serializers.CharField(max_length=50,default='')
    address_line_1=serializers.CharField(max_length=200,default='')

    class Meta:
        model = User
        fields = ('id','ngo_name','username','password','registration_number','certificate','image','contact','description','address_line_1','city','state','country','pincode')

class UserProfileSerializer(serializers.ModelSerializer):

    def newsave(self):
        user=User(username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'])
        password=self.validated_data['password']
        user.set_password(password)
        user.save()
        user_profile=UserProfile.objects.create(user=user,
                                            contact=self.validated_data['contact'],
                                            country=self.validated_data['country'],
                                            state=self.validated_data['state'],
                                            city=self.validated_data['city'],
                                            pincode=self.validated_data['pincode'],
                                            address_line_1=self.validated_data['address_line_1'])
        user_profile.save()
        return user

    contact = serializers.CharField(max_length=10,default="")
    country=serializers.CharField(max_length=50,default="")
    state=serializers.CharField(max_length=50,default="")
    city=serializers.CharField(max_length=50,default="")
    pincode=serializers.CharField(max_length=50,default="")
    address_line_1=serializers.CharField(max_length=200,default="")

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','password','contact','address_line_1','city','state','country','pincode')

class RequirementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = NgoRequirements
        fields = "__all__"

class RecieptsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reciept
        fields = "__all__"

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(style={"input_type": "password"})
