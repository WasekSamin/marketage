from django.contrib import admin
from ChatApp.models import *
# Register your models here.


admin.site.register(ChatRoom)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sent_date", "chatroom", "sender", "msg")

