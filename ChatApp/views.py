from django.shortcuts import render, HttpResponse, redirect

from ChatApp.models import ChatRoom, Message

from django.contrib.auth.models import User

from django.db.models import Q

from datetime import datetime, timedelta

from django.utils import timezone

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from mainApp.models import *

import random, string
from mainApp.models import Checkout, BuyerPostRequest
from mainApp.decorators import has_selleraccount
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# Create your views here.





@login_required(login_url='user_login')
@has_selleraccount
def home_page(request):

    all_users = User.objects.exclude(username=request.user)

    # all_users = User.objects.all()

    ct_room = ChatRoom.objects.filter(sellers=request.user).order_by("-id")

    for_buyer = ChatRoom.objects.filter(buyer=request.user).order_by("-id")

    # print(ct_room)

    args = {

        'all_users': all_users,

        'ct_room': ct_room,

        'for_buyer': for_buyer

    }

    return render(request, 'Test/index.html', args)





def create_random_chatroom_slug(str_len):

    rand_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k = str_len))

    chatroom = ChatRoom.objects.filter(slug=rand_slug)

    if chatroom.exists():

        create_random_chatroom_slug(str_len)

    return rand_slug



@login_required(login_url='user_login')
# @has_selleraccount
def user_details(request, id):

    user_details = User.objects.get(pk=id)
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
        
    buyer = request.user
    sellers = user_details.username
    sellers = User.objects.get(username=sellers)
    
    
    chatroom1 = ChatRoom.objects.filter(sellers=sellers, buyer=buyer)
    chatroom2 = ChatRoom.objects.filter(sellers=buyer, buyer=sellers)
    
    if chatroom1.exists():
        room = chatroom1.last()
        return redirect(f"/chat/chatroom/{room.id}/{room.slug}/")
    elif chatroom2.exists():
        room = chatroom2.last()
        return redirect(f"/chat/chatroom/{room.id}/{room.slug}/")


    if request.method == 'POST':
        # buyer = request.user
        # sellers = user_details.username

        try:
            sellers = User.objects.get(username=sellers)
            room_name = request.POST.get('room_name')

        except:

            return redirect("/")

        else:
            slug = create_random_chatroom_slug(20)

            room = ChatRoom(

                slug=slug, buyer=buyer, sellers=sellers, room_name=room_name

            )

            room.save()
            seller_email = sellers.email
            email_subject = "You got a new message"
            email_message = render_to_string("Test/mailview/message_mail.html",{
                "buyer": buyer,
                "sellers": sellers
            })

            email = EmailMultiAlternatives(email_subject, email_message, to=[seller_email])
            email.attach_alternative(email_message, "text/html")
            email.send(fail_silently=False)


            return redirect(f"/chat/chatroom/{room.id}/{room.slug}/")

        
    args = {

        'user_details': user_details,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
    }
    return render(request, 'Test/user_details.html', args)



@login_required(login_url='user_login')
def postChatRoomView(request, id, slug):

    msg_lst = []

    chatroom = ChatRoom.objects.get(pk=id, slug=slug)

    values = Message.objects.filter(chatroom=id)

    month_dct = {

                1: "Jan.", 2: "Feb.", 3: "March", 4: "April", 5: "May",

                6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.",

                11: "Nov.", 12: "Dec."

            }

    

    for item in values:

        send_at = item.send_date

        month = int(send_at.strftime("%m"))

        month = str(month_dct[month])

        # print(month)

        day = str(int(send_at.strftime("%d")))

        # print(day)

        year = str(send_at.strftime("%Y"))

        hour = str(send_at.strftime("%I"))

        minute = str(send_at.strftime("%M"))

        am_pm = str(send_at.strftime("%p").lower())

        

        send_at = f"{month} {day}, {year}, {hour}:{minute} {am_pm}"

        
        if item.msg:
            msgs = {
    
                "id": str(sent.id),
    
                "profile_image": str(item.sender.selleraccount.profile_picture),
    
                "message": item.msg,
    
                "username": item.sender.username,
    
                "send_at": send_at
    
            }
        elif item.attachment:
            msgs = {
    
                "id": str(sent.id),
    
                "profile_image": str(item.sender.selleraccount.profile_picture),
    
                "attachment": item.attachment,
    
                "username": item.sender.username,
    
                "send_at": send_at
    
            }

        msg_lst.append(msgs)

    return JsonResponse(msg_lst, safe=False)



@login_required(login_url='user_login')
# @has_selleraccount
def chatRoomView(request, id, slug):
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    chatroom = ChatRoom.objects.get(pk=id, slug=slug)
    # Seller Information
    seller_level = chatroom.sellers.selleraccount.level
    seller_review_count = ReviewSeller.objects.filter(seller=chatroom.sellers).count()

    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False

    try:

        chatroom = ChatRoom.objects.get(pk=id, slug=slug)

    except ChatRoom.DoesNotExist:

        return redirect("buying_view")

    else:
        if chatroom.seen is not True:
            chatroom.seen = True
            chatroom.save()

        values = Message.objects.filter(chatroom=id)

        rooms = ChatRoom.objects.filter(Q(buyer=request.user) or Q(sellers=request.user)).order_by("-id")
  

        if request.method == 'POST':

            receiver = None

            sender = request.user

            

            if sender == chatroom.sellers:

                receiver = chatroom.buyer

            else:

                receiver = chatroom.sellers

            

            msg = request.POST.get('msg')
            
            attachment = request.FILES.get("attachment")
            message = None
            
            if not msg and not attachment and len(msg) == 0:
                return redirect(f"/chat/chatroom/{chatroom.id}/{chatroom.slug}/")
            
            if msg != None:
                msg = msg.strip()
                
                if len(msg) == 0:
                    return
                
                sent = Message(sender=sender, receiver=receiver, msg=msg, chatroom=chatroom)
            elif attachment != None:
                Message.objects.create(sender=sender, receiver=receiver, attachment=attachment, chatroom=chatroom)
                return redirect(f"/chat/chatroom/{chatroom.id}/{chatroom.slug}/")

    
            chatroom.seen = False
            chatroom.recent_chat = True

            chatroom.save()

            sent.save()

    

            # print("IMAGE:", str(sender.selleraccount.profile_picture))

            # print("USER:", sender)

            # print("MESSAGE:", msg)

    

            if request.is_ajax():

                month_dct = {

                    1: "Jan.", 2: "Feb.", 3: "March", 4: "April", 5: "May",

                    6: "June", 7: "July", 8: "Aug.", 9: "Sept.", 10: "Oct.",

                    11: "Nov.", 12: "Dec."

                }

    

                send_at = sent.sent_date

                month = int(send_at.strftime("%m"))

                month = str(month_dct[month])

                # print(month)

                day = str(int(send_at.strftime("%d")))

                # print(day)

                year = str(send_at.strftime("%Y"))

                hour = str(send_at.strftime("%I"))

                minute = str(send_at.strftime("%M"))

                am_pm = str(send_at.strftime("%p").lower())

                

    

                # send_at = send_at.strftime("%b %d, %Y, %I:%M %p")

                send_at = f"{month} {day}, {year}, {hour}:{minute} {am_pm}"

                profile_image = str(sender.selleraccount.profile_picture)

    
                if msg != None:
                    message = {
    
                        "id": str(sent.id),
    
                        "profile_image": profile_image,
    
                        "message": msg,
    
                        "username": sender.username,
    
                        "send_at": send_at
    
                    }
                elif attachment != None:
                    message = {
    
                        "id": str(sent.id),
    
                        "profile_image": profile_image,
    
                        "attachment": attachment,
    
                        "username": sender.username,
    
                        "send_at": send_at
    
                    }

    

                # print("MESAGE", message)

                # print("AFTER:", len(Message.objects.all()))

    

                # x =  str(Message.objects.all())

                # print(Message.objects.values())

    

                data = {

                    "message_info": message

                }

                return JsonResponse(data)

            return redirect(f"/chat/chatroom/{chatroom.id}/{chatroom.slug}/")

    

    

    args = {

        'chatroom': chatroom,

        'values': values,

        'rooms': rooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "seller_level": seller_level,
        "seller_review_count": seller_review_count
        # 'ago': ago

    }

        

    # print(chatroom)

    return render(request, "Test/chatRoom.html", args)
    
    
# Download Function
@login_required(login_url='user_login')
# @has_selleraccount
def download(request, path):
    attachment = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(attachment):
        with open(attachment, "rb") as fh:
            response = HttpResponse(
                fh.read(), content_type="application/attachment")
            response["Content-Disposition"] = "inline;filename=" + \
                os.path.basename(attachment)
            return response
    raise Http404