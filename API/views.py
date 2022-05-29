from rest_framework.serializers import Serializer

from API.serializers import ServiceSerializer

from mainApp.models import Services

from django.http import response

from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from mainApp.models import *

from .serializers import *

from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication

from rest_framework import status





class ServiceApiView(APIView):

    def get(self, request):

        services = Services.objects.all()

        data = []

        serializer = ServiceSerializer(services, many=True)



        return Response(serializer.data)





class OfferApiView(APIView):
    def get(self, request):

        offers = Offer.objects.filter(offer_status="ACTIVE").order_by("-click")

        serializer = OfferSeriaLizer(offers, many=True)


        return Response(serializer.data)





class OfferFavoriteView(APIView):

    permission_classes = [IsAuthenticated, ]

    authentication_classes = [TokenAuthentication, ]



    def post(self, request):

        data = request.data['id']



        try:

            offer_obj = Offer.objects.get(id=data)



            user = request.user



            single_interested_offer = OfferFavoriteModel.objects.filter(user=user).filter(

                offer=offer_obj

            )



            if single_interested_offer:

                print(single_interested_offer)

                var = single_interested_offer.is_interested

                single_interested_offer.is_interested = not var

                single_interested_offer.save()

            else:

                OfferFavoriteModel.objects.create(

                    offer=offer_obj, user=user, is_Favorite=True

                )



            respose_msg = {'error': False}



        except:

            response_msg = {'error': True}



        return Response(response_msg)





class CategoryView(APIView):

    # permission_classes = [IsAuthenticated, ]

    # authentication_classes = [TokenAuthentication, ]



    def get(self, request):

        category = Category.objects.all()



        data = []



        serializer = CategorySerializer(category, many=True)

        # user = request.user

        # for category in serializer.data:

        #     interested_query = CategoryInterestedModel.objects.filter(user=user).filter(

        #         category_id=category['id']

        #     )



        #     if interested_query:

        #         category['categoryinterestedmodel'] = interested_query[0].is_interested

        #     else:

        #         category['categoryinterestedmodel'] = False

        #     data.append(category)



        return Response(serializer.data)





class CategoryInterestedView(APIView):

    permission_classes = [IsAuthenticated, ]

    authentication_classes = [TokenAuthentication, ]



    def post(self, request):

        data = request.data['id']



        try:

            category_obj = Category.objects.get(id=data)

            user = request.user

            single_interested_category = CategoryInterestedModel.objects.filter(

                user=user

            ).filter(category=category_obj).first()



            if single_interested_category:

                print("single_iterested_category")

                var = single_interested_category.is_interested

                single_interested_category.is_interested = not var

                single_interested_category.save()

            else:

                CategoryInterestedModel.objects.create(

                    category=category_obj, user=user, is_interested=True

                )



            respose_msg = {'error': False}

        except:

            response_msg = {'error': True}



        return Response(response_msg)







class BuyerPostRequestView(APIView):

    permission_classes = [IsAuthenticated, ]

    authentication_classes = [TokenAuthentication, ]

    def get(self, request):

        data = []

        buyer_post = BuyerPostRequest.objects.all()

        

        serializer = BuyerPostSerializer(buyer_post, many=True)

        

        return Response(serializer.data)

        
# Message API View

class MessageView(APIView):



    def get(self, request):

        data = []

        # messages = Message.objects.filter(sender=request.user)

        messages = Message.objects.all()



        message_serializer = MessageSerializer(messages, many=True)

        return Response(message_serializer.data)

        

        

    def post(self, request, format=None):

        post_serializer = MessageSerializer(data=request.data)

        if post_serializer.is_valid():

            post_serializer.save()

            return Response(post_serializer.data, status=status.HTTP_201_CREATED)

        return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        

class OfferDetailsView(APIView):
    def get(self, request, id):
        data = []
        offer_details = Offer.objects.get(pk=id)
        offer_details_serializer = OfferSeriaLizer(offer_details, many=False)
        return Response(offer_details_serializer.data)
        


class CategoryWiseOffersView(APIView):
    def get(self, request):
        query = Category.objects.all()
        serializer = CategoryWiseOfferSerializer(query, many=True)
        return Response(serializer.data)


class SubcategoryView(APIView):
    def get(self, request):
        query = Subcategory.objects.all()
        serializer = SubcategorySerializer(query, many=True)
        return Response(serializer.data)
        
        
        
        
        
        
class ChildSubcategoryView(APIView):
    def get(self, request):
        query = ChildSubcategory.objects.all()
        serializer = ChildSubcategorySerializer(query, many=True)
        return Response(serializer.data)
        
        
        
class SellerAccountView(APIView):
    # permission_classes = [IsAuthenticated, ]
    # authentication_classes = [TokenAuthentication, ]
    def get(self, request):
        try:
            query_obj = SellerAccount.objects.all()
            serializer = SellerAccountSerializer(query_obj, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except SellerAccount.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
        

class OfferManagerView(APIView):
    def get(self, request, offer_id):
        try:
            offerId = Offer.objects.get(pk=offer_id)
            query_obj = OfferManager.objects.filter(id=offerId.id)
            serializer = OfferManagerSerializer(query_obj, many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except OfferManager.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        