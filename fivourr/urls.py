from django.contrib import admin
from django.urls import path, include
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.static import serve


urlpatterns = [
    path('musharaf/', admin.site.urls),
    path('adminpanel/', include('AdminPanel.urls')),

    # Password Reset URL
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="accountview/password_reset.html"), name="reset_password",),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="accountview/email_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accountview/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accountview/reset_password_complete.html"), name="password_reset_complete"),
    
    # Email Verification Path
    path("verifiy/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    
    # Campaign page url
    path("campaign/", views.campaignPageView, name="campaign"),

    # azim url of reset
    path ("password_reset_confirm/", views.password_reset_confirm, name="password-reset-confirm"),
    
    # Exam success url
    path("exam-succes", views.examSuccessView, name="exam-success"),
    
    # Chat App URLS
    path('chat/', include('ChatApp.urls')),
    # Inbox
    path("inbox", views.chatInbox, name="inbox"),
    # Buyer Chat url
    path("buyer_chat/", views.buyer_chat_messages, name="BuyerChat"),
    
    # API PATH

    path('api/', include('API.urls')),

    path('', views.get_landing_page, name="get_landing_page"),
    path('buyer_view/', views.buying_view, name="buying_view"),
    path('offer_details/<int:id>/<str:slug>/', views.offer_details, name="offer_details"),

    #user Registration URL
    path('registration/', views.user_registration, name="user_registration"),
    # User Login URL

    path('login/', views.user_login, name="user_login"),

    # Logout URL

    path('logoutview/', views.logoutview, name="logoutview"),
    
    # Review success url
    path("review-success/", views.reviewSuccessView, name="review-success"),

    ## Seller Profile View URL

    path('seller_profile/', views.seller_profile, name="seller_profile"),

    ## Service wise offers url
    path('service-wise/<str:slug>/', views.service_wise_offers, name="service_wise_offers"),
    # Category wise page
    path("category-wise/<slug:slug>/", views.category_wise_offers, name="category-wise"),
    # Manage order page url
    path("manage-order/", views.manageOrder, name="manage-order"),
    # offers page url
    path("manage-offers/", views.manageOffers, name="manage-offers"),
    # Notify offer
    # path("notify-offer/", views.get_notificationOffer, name="notify-offer"),
    # Offer paused url
    path("paused-offer/<int:id>/", views.pausedOffer, name="pausedOffer"),
    # Offer delete url
    path("delete-offer/<int:id>/", views.deleteOffer, name="deleteOffer"),
    # Seller Dashboard
    path('seller_dashboard/', views.seller_dashboard, name="seller_dashboard"),

    # cart page or checkout Page

    path('cart/', views.cartView, name="cartView"),

    # Add To Cart

    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),

    # Checkout Page Url
    path('checkout/', views.checkout, name="checkout"),

    # category wise Subcategory
    # path('category_wise_offers/p=2021/<int:category_id>/', views.category_wise_offers, name="categoryWiseView"),

    # Subcategory Wise Offer URL
    path("subcategory/<str:slug>/", views.subcategory_wise_offers, name="SubcategoryWiseOffer"),

    # Settings URL
    path('settings/', views.settings_page, name="settings"),

    # Account url
    path('account/<int:user_id>/<str:user_username>/', views.account_detailsView, name="account"),

    # security url
    path('security/', views.security_page, name="security_page"),

    # notifications_page url

    path('notifications/', views.notifications_page, name="notifications_page"),


    # support page url

    path('support/', views.support_page, name="support"),

    # Contacts Page Url

    path('contacts/', views.azim_contact_page, name="contact"),

    # All Category Page Url
    path('categories/', views.view_all_category, name="Categories"),

    # POST A REQUEST PAGE URL
    path('post_request/', views.post_a_request, name="post_a_request"),
    # Add post request
    path("added-post-request/", views.added_post_request, name="added-post-request"),

    #  Become A Seller Page

    path('become_a_seller/', views.get_become_a_seller_page, name="BecomeSeller"),

    # Buyer Orders Page Url
    
    path('buyer_orders/', views.get_buyer_orders_url, name="BuyerOrders"),
    
    # Order Details Page URL
    
    path('order_details/<int:id>/<str:slug>/', views.get_order_details_url, name="OrderDetails"),
    
    # Pay With SSLCOMMERZ URL
    
    # path('sslcommerz_payment/', views.pay_with_sslcommerz, name="SSLCOMMERZ"),

    # Success page
    path("success/", views.successView, name="success"),
    # Failed page
    path("failed/", views.failedView, name="failed"),
    # Cancelled page
    path("cancelled/", views.cancelledView, name="cancelled"),
    # Extended user page
    path("extended-user/", views.extendedUserView, name="extended-user"),
    # Seller submit page
    path("seller-submit/<int:pk>/<str:slug>/", views.sellerSubmitView, name="seller-submit"),
    # About us page
    path("about-us/", views.aboutusView, name="about-us"),
    
    path("privacy-policy/", views.privacypolicyView, name="privacypolicy"),
    
    path("help-support/", views.helpSupportView, name="helpSupport"),
    
    path("trust-safety/", views.trustSafetyView, name="trustSafety"),
    
    path("term-of-services/", views.termOfservicesView, name="termOfservices"),

    # Create offer page
    path("create-offer/", views.createOfferView, name="create-offer"),
    # Edit Offer Page
    path('edit_offer/<int:id>/<str:slug>/', views.edit_offer, name="EditOffer"),
    # Buyer orders page
    path("buyer-orders/<int:pk>/<str:slug>/", views.buyerOfferFormView, name="buyer-orders"),
    # Buyer dashboard page
    path("buyer-dashboard/", views.buyerDashboardFormView, name="buyer-dashboard"),
    # Seller ORder Details
    path('seller_order_details/<int:id>/', views.seller_order_details, name="SellerOrderDetails"),
    # Search page
    path("search/", views.searchPageView, name="search"),
    # Send offer form
    path("send-offer/<int:id>/", views.sellerSendOfferView, name="send-offer"),
    # Buyer requested post
    path("buyer-posts/", views.buyerAllPostsView, name="buyer-posts"),
    # Delete a requested post
    path("delete-buyer-post/<int:id>/", views.deleteBuyerPost, name="delete-buyer-post"),
    # Reserved a requested post
    path("reserved-buyer-post/<int:id>/", views.reservedBuyerPost, name="reserved-buyer-post"),
    # Active a requested post
    path("active-buyer-post/<int:id>/", views.activeBuyerPost, name="active-buyer-post"),
    # Refund request page
    path("refund-request/", views.refundRequestView, name="refund-request"),
    # Payment terms page
    path("payment-terms/", views.payemntTermsView, name="payment-term"),
    # Question page
    path("pre-exam-submit/", views.preExamSubmission, name="pre-exam-submit"),
    # Exam page
    # path("exam/", views.examView, name="exam"),

    # Test URL
 
    
    # Buyer Request URL
    path("buyer_requests/", views.buyer_requestView, name="BuyeRequestView"),
    # My Contacts Page
    path("my_contacts/", views.my_contacts_page, name="my_contacts_page"),

    # Earnings Page url
    path("earnings/<int:id>/", views.earnings, name="earnings"),

    # Buyer Review Seller page URL
    path("review_seller/<str:username>/", views.reviewSellerForm, name="ReviewSeller"),
    
    
    # Complete Paypal URL

    path("paypal_success/<int:id>/", views.paypal_success, name="paypal_success"),
    
    # Test Purpose
    path("all_test_orders/", views.all_test_orders, name="allTestOrders"),

    # Test Reafun Part
    path("rafsun/", views.rafsun_header, name="rafsun"),

    # SELECT QUSTION'S SUBJECT URL
    path("subjects/", views.select_subject_form, name="select_subject_form"),
    # Exam Room URL
    path("exam-room/<int:id>/", views.subject_wise_exam_qustion, name="Exam"),
    # Subject wise qustion url
    # path("exam-room/<int:subject_id>/", views.exam_room, name="exam-room"),
    # Review Path
    path("review/<int:checkout_id>/", views.review_offer, name="ReviewOffer"),

    # Premium Packge VIew URl
    path("premium-packages/", views.premium_offer_package_view, name="PremiumOfferPackageView"),
    # Add Premium Package To Cart URL
    path("add_package_to_cart/", views.add_package_to_cart, name="add_package_to_cart"),
    # PACKAGE CHECKOUT URL
    path("package-checkout/", views.premium_direct_checkout, name="premium_direct_checkout"),
    # Premium Payment URL
    path("payment/<int:id>/", views.premium_payment, name="PremiumPayment"),

    # PRemium Checkout Response Views
    path("premium-success/", views.premium_successView, name="PremiumSuccessview"),
    path("premium-cancel/", views.premiumfailedView, name="PremiumFailedView"),
    path("premium-failed/", views.premiumcancelledView, name="PremiumCancelView"),
    # 404 page url
    path("page-404/", views.page_404View, name="page-404"),
    # Child Wise Offers
    path("child-wise-offers/<int:id>/<slug:slug>/", views.get_child_category_wise_offers, name="ChildWiseOffers"),
    
    # manualPayment URL
    path("bkash-nagad/<int:id>/", views.pay_manually, name="pay_manually"),
    
        # Campaign page URL
    path("campaigns/", views.campaignPageView, name="get_campaign_page"),
    # Campaign Wise Qustion URL
    path("campaigns-wise-qustion/<int:id>/", views.get_campaigns_qustion_submit_answer, name="CampaignWiseQustion"),
    # Response success URL
    path("response-success/", views.get_success_response, name="success-response"),
    
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)