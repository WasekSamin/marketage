from django.urls import path

from django.conf.urls.static import static

from .views import (BuyerPostRequestView, CategoryInterestedView,
    CategoryView, ServiceApiView, OfferApiView, MessageView, CategoryWiseOffersView, OfferDetailsView, SubcategoryView, ChildSubcategoryView, SellerAccountView, OfferManagerView)



from rest_framework.authtoken.views import obtain_auth_token




urlpatterns = [

    path('services/', ServiceApiView.as_view()),

    path('offers/', OfferApiView.as_view()),

    path('category/', CategoryView.as_view()),

    path('interested_category/', CategoryInterestedView.as_view()),

    path('buyer_posts/', BuyerPostRequestView.as_view()),
    
    path('messages/', MessageView.as_view()),

 
    # Offer Details APIView
    path("offer-details/<int:id>/", OfferDetailsView.as_view()),
    # Category Wise Offers
    path("category-wise-offers/", CategoryWiseOffersView.as_view()),
    # Subcategory api url
    path("sub-category/", SubcategoryView.as_view()),
    
    #child sub category api url
    path("child-subcategory/", ChildSubcategoryView.as_view()),
    
    # Selleracccount urls
    path("selleraccounts/", SellerAccountView.as_view()),
    # OfferManager urls
    path("offer-manager/<int:offer_id>/", OfferManagerView.as_view()),

]

