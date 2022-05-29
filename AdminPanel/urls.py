from django.urls import path, include
from AdminPanel import views


urlpatterns = [
    path('', views.get_adminpanel_url, name="AdminHome"),

    # Order Details URL
    path("order_details/<int:id>/", views.order_details, name="order_details"),

    path("uploaded-offer/", views.uploadedOfferView, name="uploaded-offer"),
    path("all-users/", views.allUsersView, name="all-users"),
    path("all-orders/", views.allOrdersView, name="all-orders"),
    path("admin-login/", views.adminLoginView, name="admin-login"),
    # Admin Logout
    path("admin-logout/", views.adminlogoutview, name="adminlogoutview"),
    path("transaction/", views.transactionView, name="TransactionView"),
    path("update_offer/<int:id>/<str:slug>/", views.admin_edit_offer, name="AdminUpdateOffer"),
    path("withdraw-view/", views.withdrawView, name="WithdrawView"),
    path("withdraw-details/<int:id>/", views.clear_amount, name="clear_amount"),
    # Get Exam Room URL
    path("exam-room-review/", views.get_exam_room_page, name="EXAMROOM"),
    # GET EXAM ROOM DETAILS URL
    path("exam-answer-details/<int:id>/", views.get_exam_room_details_url, name="Answer"),

    # NOTIFICATION URL
    path("notifications/", views.get_notification, name="notificationView"),
    # Notification Details URl
    path("notification-details/<int:id>/", views.get_notificatiion_details_url, name="NotificationDetails"),
    
    # Manual Transaction URL
    
    path("get_manual_transaction_page/", views.get_manual_transaction_page, name="get_manual_transaction_page"),
    
    # manual payment Details
    path("update_manual_payment/<int:id>/", views.update_manual_payment, name="update_manual_payment"),

    # path(),
    # Sending Email to Users
    path("send-email-to-users/", views.send_email_to_user, name="send_email_to_user"),
]