from django.urls import path, include
from ChatApp import views


urlpatterns = [
    path("test_home/", views.home_page, name="home_page"),
    path("welcome_room/<int:id>/", views.user_details, name="user_details"),
    path("chatroom/<int:id>/<str:slug>/", views.chatRoomView, name="chatroom"),
    path("post-chat/<int:id>/<str:slug>/", views.postChatRoomView, name="post-chat"),
    # path("view_profile/<int:id>/", views.user_details, name="user_details"),
    # # path("form_validation/", views.form_validation, name="form_validation"),
    # path("room/", views.room, name="room"),
    # path("chatting/<int:id>", views.continue_chat, name="continueChat")
]
