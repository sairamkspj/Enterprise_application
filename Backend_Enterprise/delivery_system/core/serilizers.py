from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer): 

    Restarent_name= serializers.CharField(required=False,allow_blank=True)
    Contact_number= serializers.CharField(required=False,allow_blank=True)
    Location= serializers.CharField(required=False,allow_blank=True)

    password = serializers.CharField(write_only=True)  # ensure password is write_only
    class Meta:
        model=User
        fields=['username','password','email','role','Restarent_name','Contact_number','Location']
        extra_kwargs={'password':{'write_only':True}}

    def create(self, validated_data):

        restaurant_name = validated_data.pop("Restarent_name", "")
        location = validated_data.pop("Location", "")
        contact_number = validated_data.pop("Contact_number", "")

        user=User.objects.create_user(**validated_data)

        # if user.role == 'vendor':
        #     Vendor.objects.create(user=user,Restarent_name=restaurant_name,Location=location,Contact_number=contact_number)

        return user
