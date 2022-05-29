from rest_framework import serializers

from mainApp.models import BuyerPostRequest, Category, Services, Offer, Subcategory, ChildSubcategory, SellerAccount, OfferManager

from django.contrib.auth.models import User
from ChatApp.models import Message

from rest_framework.authtoken.models import Token


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Services

        fields = '__all__'





class OfferSeriaLizer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'offer_title', 'image', 'user', 'click', 'category', 'packages')
        depth = 1
        


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:

        model = Category

        fields = '__all__'





class CategoryWiseOfferSerializer(serializers.ModelSerializer):
    offers = serializers.StringRelatedField(many=True)

    class Meta:

        model = Category

        fields = ['id', 'title', 'icon', 'offers']

        





class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = '__all__'

        

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        Token.objects.create(user=user)

        return user





class BuyerPostSerializer(serializers.ModelSerializer):

    class Meta:

        model = BuyerPostRequest

        fields = '__all__'

        
## MEssage Serializer ##

class MessageSerializer(serializers.ModelSerializer):

    class Meta:

        model = Message

        fields = '__all__'

        depth = 2



class CategoryWiseSerializer(serializers.ModelSerializer):

    class Meta:

        model = Offer
        fields = '__all__'
        depth = 2
        
        

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ['id', 'sub_title', 'sub_img']
        
        

class ChildSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildSubcategory
        fields = '__all__'
        depth = 1


class SellerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerAccount
        fields = ("joined_at", "user", "contact_no", "profile_picture", "country", "level", "withdrawn")
        depth = 1
    
    
class OfferManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferManager
        fields = "__all__"
        depth = 1
    
    