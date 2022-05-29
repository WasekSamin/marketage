from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Avg, Max, Min
from django.contrib import messages
from .models import *
import time
import os, uuid
from .forms import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import date
from datetime import datetime, timedelta
import string
import random
from ChatApp.models import *
from django.core.mail import send_mail
from decimal import Decimal
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from .decorators import has_selleraccount
import uuid
from django.core.mail import EmailMultiAlternatives



def get_landing_page(request):
    main_logo = MainLogo.objects.all()
    # print(main_logo)
    user_session = request.session.get("user", None)
    # print(f"{user_session}")
    premium_offers = Offer.objects.filter(is_premium=True, offer_status="ACTIVE")

    if (user_session is None):
        landing_slider = LandingSlider.objects.all().order_by('-id')
        services = Services.objects.all()
        cats = Category.objects.all()
        subcats = Subcategory.objects.all()

        args = {
            'landing_slider': landing_slider,
            'services': services,
            'cats': cats,
            'main_logo': main_logo,
            "premium_offers": premium_offers
        }
        return render(request, 'landingview/landingPage.html', args)
    else:
        return redirect("buying_view")


# landing Service Wise Offer Page 
@login_required(login_url='user_login')
def service_wise_offers(request, slug):
    try:
        single_service = Services.objects.get(slug=slug)
    except Services.DoesNotExist:
        return redirect("buying_view")
    
    all_offers = Offer.objects.filter(offer_status="ACTIVE", service__slug=slug)
    
    main_logo = MainLogo.objects.all().last()
    service = Services.objects.all()
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by("-click")
    cats = Category.objects.all().order_by("-id")[:9]
    order_seen = True
    
    user_session = request.session.get("user", None)
    all_seller_offers_seen = True
    order_seen = True
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
    
    args = {
        "single_service": single_service,
        'service': service,
        'offers': offers,
        "all_offers": all_offers,
        'cats': cats,
        'main_logo': main_logo,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }

    return render(request, 'landingview/service_wise_offers.html', args)




@login_required(login_url='user_login')
@has_selleraccount
def view_all_category(request):
    offers = Offers.objects.filter(offer_status="ACTIVE").order_by("-click")
    main_logo = MainLogo.objects.all().last()
    cats = Category.objects.all().order_by("-id")[:9]
    categories = Category.objects.all().order_by('id')
    
    if request.user != None:
        order_seen = True
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
        if len(orders):
            order_seen = False

    args = {
        'cats': cats,
        'main_logo': main_logo,
        "categories": categories,
        "order_seen": order_seen,
        "offers": offers,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }

    return render(request, 'landingview/categories.html', args)


@login_required(login_url='user_login')
@has_selleraccount
def buying_view(request):
    all_premium_offers = []
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
    
    main_logo = MainLogo.objects.all().last()
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    cats = Category.objects.all().order_by("-id")[:9]

    subs = Subcategory.objects.all()

    # for item in cats:
    #     print(item)
    #     print(len(item.subcategory.all()))

    # pop_offers = Offer.objects.filter(is_popular=True).order_by('?')
    pop_web_offers = Offer.objects.filter(is_pro=True, offer_status="ACTIVE").order_by('?')

    premium_offers = Offer.objects.filter(is_premium=True, offer_status="ACTIVE").order_by('?')

    dt_now = datetime.now()
    dt_now = datetime.strftime(dt_now, "%Y-%m-%d %H:%M:%S")
    dt_now = datetime.strptime(dt_now, "%Y-%m-%d %H:%M:%S")

    # print("DT NOW:", dt_now)

    for item in premium_offers:
        expired_datetime = None
        if item.is_bronze == True:
            expired_datetime = item.bronze_created + timedelta(days=4)
        elif item.is_silver == True:
            expired_datetime = item.silver_created + timedelta(days=8)
        elif item.is_gold == True:
            expired_datetime = item.gold_created + timedelta(days=31)

        # print("EXPIRED DATETIME:", expired_datetime)
        
        if expired_datetime is not None:
            expired_datetime = datetime.strftime(expired_datetime, "%Y-%m-%d %H:%M:%S")
            # print(expired_datetime)
            expired_datetime = datetime.strptime(expired_datetime, "%Y-%m-%d %H:%M:%S")
            # print(expired_datetime)
    
            if dt_now < expired_datetime:
                all_premium_offers.append(item)

    # print("ALL PREMIUM OFFERS:", all_premium_offers)

    args = {
        'offers': offers,
        # 'pop_offers': pop_offers,
        'cats': cats,
        'pop_web_offers': pop_web_offers,
        'main_logo': main_logo,
        "all_premium_offers": all_premium_offers,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "order_seen": order_seen,
        "subs": subs,
        "all_seller_offers_seen": all_seller_offers_seen,
    }
    return render(request, 'buyingview/buying_view.html', args)

@login_required(login_url='user_login')
@has_selleraccount
def offer_details(request, id, slug):
    cats = Category.objects.all().order_by("-id")[:9]
    offer = Offer.objects.filter(id=id, slug=slug).first()
    
    if offer.offer_status != "ACTIVE":
        return redirect("buying_view")
    
    review_sellers = ReviewSeller.objects.filter(seller=offer.user)

    cart_session = request.session.get("cart", None)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False

    # print("Offer er owner:" + str(offer.user))

    if offer.user != request.user and offer.already_clicked == False:
        offer.click += 1
        offer.already_clicked = True
        offer.save()
        # giving Points to The Owner of the User
        for i in range(offer.click):
            if offer.click <= 9999:
                offer.points += i
                offer.save()
    args = {
        'offer': offer,
        'cats': cats,
        "cart_session": cart_session,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "review_sellers": len(review_sellers),
    }
    return render(request, 'buyingview/offers_details.html', args)


def user_registration(request):
    user_session = request.session.get("user", None)
    if (user_session is None):
        form = UserRegistration()
        if request.method == 'POST':
            form = UserRegistration(request.POST)
            if form.is_valid():
                request.session["new_user"] = True
                current_site = get_current_site(request)
                user = form.save(commit=False)
                user.is_active = False
                user.save()
    
                mail_subject = "Account Verification Link"
                message = render_to_string("accountview/verify.html", {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail = form.cleaned_data.get('email')
                email = EmailMultiAlternatives(mail_subject, message, to=[send_mail])
                email.attach_alternative(message, "text/html")
                email.send()
    
                messages.success(request, "Email Sent Please verify your account")
                messages.info(request, "Please Activate Your Account ASAP")
    
                return redirect('user_login')
    else:
        return redirect("buying_view")
    args = {
            'form': form,
            # 'user': user,
        }
    return render(request, 'accountview/registration.html', args)
    # else:
    #     return redirect("buying_view")



# User Registration Function
UserModel = get_user_model()
def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        # user = UserModel._default_manager.get(pk=uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is now activated or verified")
        return redirect("user_login")
    else:
        # messages.warning(request, "Invalid Activaton Link Please Try again later")
        # return redirect("user_registration")
        return HttpResponse("Activation Link is invalid")


def user_login(request):
    user_session = request.session.get("user", None)
    new_user = request.session.get("new_user", None)

    if (user_session is None):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Creating user session
                user_session = username
                request.session["user"] = user_session
                login(request, user)
                # print("USER SESSION:")
                # print(request.session.get("user"))
                if new_user is not None:
                    return redirect("extended-user")
                return redirect('buying_view')
            else:
                messages.error(request, "Incorrect username or password!")

        return render(request, 'accountview/login.html')
    else:
        return redirect("buying_view")


def logoutview(request):
    logout(request)
    return redirect('get_landing_page')


@login_required(login_url='user_login')
@has_selleraccount
def seller_profile(request):
    return render(request, 'accountview/seller.html')


# Order page
@login_required(login_url='user_login')
@has_selleraccount
def manageOrder(request):
    dt_now = datetime.now() - timedelta(days=1)
    dt_now = datetime.strftime(dt_now, "%Y-%m-%d %H:%M:%S")
    dt_now = datetime.strptime(dt_now, "%Y-%m-%d %H:%M:%S")
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    for item in not_seen_orders:
        if item.order_is_seen == False:
            item.order_is_seen = True
            item.save()
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    
    cats = Category.objects.all().order_by("-id")[:9]
    orders = Checkout.objects.filter(seller=request.user, paid=True).order_by("-id")
    active_orders, late_orders, delivered_orders, completed_orders, cancelled_orders, review_orders = [], [], [], [], [], []
    
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)

    for order in orders:
        if order.is_submitted == False:
            expired_datetime = order.due_date
            expired_datetime = datetime.strftime(expired_datetime, "%Y-%m-%d %H:%M:%S")
                # print(expired_datetime)
            expired_datetime = datetime.strptime(expired_datetime, "%Y-%m-%d %H:%M:%S")
            
            if dt_now > expired_datetime:
                order.order_status = "LATE"
                order.save()
        
        if order.is_complete:
            completed_orders.append(order)
        if order.on_review and order.order_status == "ON REVIEW":
            review_orders.append(order)
        if order.order_status == "ACTIVE":
            active_orders.append(order)
        elif order.order_status == "LATE":
            late_orders.append(order)
        elif order.order_status == "DELIVERED":
            delivered_orders.append(order)
        elif order.order_status == "CANCELLED":
            cancelled_orders.append(order)

    # print(review_orders)
    # print(cancelled_orders)

    args = {
        "active_orders": active_orders,
        "late_orders": late_orders,
        "delivered_orders": delivered_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "review_orders": review_orders,
        "cats": cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
    }

    return render(request, "wasekPart/manage_order.html", args)


# offers page
@login_required(login_url='user_login')
@has_selleraccount
def manageOffers(request):
    cats = Category.objects.all().order_by("-id")[:9]
    offers = Offer.objects.filter(user=request.user).order_by("-id")
    active_offers, pending_approvals, required_modifications, denieds, pauseds = [], [], [], [], []
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)

    for offer in offers:
        if offer.offer_status == "ACTIVE":
            active_offers.append(offer)
        elif offer.offer_status == "PENDING APPROVAL":
            pending_approvals.append(offer)
        elif offer.offer_status == "REQUIRED MODIFICATION":
            required_modifications.append(offer)
        elif offer.offer_status == "DENIED":
            denieds.append(offer)
        elif offer.offer_status == "PAUSED":
            pauseds.append(offer)

    args = {
        "offers": offers,
        "active_offers": active_offers,
        "pending_approvals": pending_approvals,
        "required_modifications": required_modifications,
        "denieds": denieds,
        "pauseds": pauseds,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "cats": cats,
    }
    return render(request, "wasekPart/manage_offers.html", args)
    

@login_required(login_url='user_login')
@has_selleraccount
def pausedOffer(request, id):
    if request.method == "POST":
        offer_id = request.POST.get("offer_id", None)
        # print(f"{offer_id}")

        if offer_id is not None:
            try:
                offer_id = int(offer_id)
            except:
                return redirect("manage-offers")
            else:
                try:
                    offer = Offer.objects.get(id=offer_id)
                    offer.offer_status = "PAUSED"
                    offer.save()
                    return redirect("manage-offers")
                except:
                    return redirect("manage-offers")
        else:
            return redirect("manage-offers")
        

@login_required(login_url='user_login')
@has_selleraccount
def deleteOffer(request, id):
    if request.method == "POST":
        try:
            offer = Offer.objects.get(id=id)
        except Offer.DoesNotExist:
            return redirect("manage-offers")
        else:
            offer.delete()
            return redirect("manage-offers")
# Chat inbox
@login_required(login_url='user_login')
@has_selleraccount
def chatInbox(request):
    cats = Category.objects.all().order_by("-id")[:9]
    all_rooms = ChatRoom.objects.filter(sellers=request.user).order_by("-id")
    
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    args = {
        "all_rooms": all_rooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "cats": cats,
    }
    return render(request, "wasekPart/chat_inbox.html", args)


# Buyer Chat
@login_required(login_url='user_login')
@has_selleraccount
def buyer_chat_messages(request):
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
        
    all_rooms = ChatRoom.objects.filter(buyer=request.user).order_by("-id")
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    args = {
        'all_rooms': all_rooms,
        "cats": cats,
        "all_seller_offers_seen": all_seller_offers_seen,
        "offers": offers,
        "order_seen": order_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
    }
    return render(request, "buyingview/buyer_chat.html", args)




# Seller Dashboard


@login_required(login_url='user_login')
@has_selleraccount
def seller_dashboard(request):
    users = User.objects.all()
    active_orders, completed_orders, cancelled_orders = [], [], []
    count_active = Checkout.objects.filter(order_status="ACTIVE").filter(user=request.user).count()
    orders = Checkout.objects.filter(seller=request.user).filter(paid=True).order_by("-id")
    cats = Category.objects.all().order_by("-id")[:9]
    
    active_offers = Offer.objects.filter(offer_status="ACTIVE", user=request.user)
    pending_offers = Offer.objects.filter(offer_status="PENDING APPROVAL", user=request.user)
    
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    # Reviews
    # review = ReviewSeller.objects.filter(seller=request.user)
    review_count = ReviewSeller.objects.filter(seller=request.user).count()
    
    # chatrooms = ChatRoom.objects.all()
    chatrooms = ChatRoom.objects.filter(Q(buyer=request.user) | Q(sellers=request.user)).order_by("-id")[:10]
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)

    for order in orders:
        if order.is_complete:
            completed_orders.append(order)
        elif order.order_status == "ACTIVE":
            active_orders.append(order)
        elif order.order_status == "CANCELLED" and order.is_cancel:
            cancelled_orders.append(order)
            
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    args = {
        'users': users,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "count_active": count_active,
        "chatrooms": chatrooms,
        "cats": cats,
        "review_count": review_count,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "active_offers": active_offers,
        "pending_offers": pending_offers,
    }

    return render(request, 'sellingview/seller_dashboard.html', args)


# Settings Page
@login_required(login_url='user_login')
@has_selleraccount
def settings_page(request):
    return render(request, 'sellingview/settings.html')

# Security Page

def examView(request):
    return render(request, "azimpart/exam.html")
    
def preExamSubmission(request):
    return render(request, "azimpart/pre_exam_submit.html")


@login_required(login_url='user_login')
@has_selleraccount
def security_page(request):
    return render(request, 'sellingview/security.html')

# Notification Page


@login_required(login_url='user_login')
@has_selleraccount
def notifications_page(request):
    return render(request, 'sellingview/notifications.html')

# Support Page


@login_required(login_url='user_login')
@has_selleraccount
def support_page(request):
    return render(request, 'azimpart/help-support.html')

# Azim Contact Page


@login_required(login_url='user_login')
@has_selleraccount
def azim_contact_page(request):
    return render(request, 'sellingview/contacts.html')


# seller Dashboard End
@login_required(login_url='user_login')
@has_selleraccount
def add_to_cart(request):
    cart = request.session.get('cart')
    remove = request.POST.get('remove')
    package_id = request.POST.get('package_id')

    if request.method == "POST":
        if cart:
            quantity = cart.get(package_id)
            if quantity:
                cart[package_id] = quantity + 1
            else:
                cart[package_id] = 1
        else:
            cart = {}
            cart[package_id] = 1
        request.session['cart'] = cart

        return redirect('cartView')


def map_function(request, package_id):
    cart = request.session.get('cart', None)
    package_id = str(package_id.id)

    if package_id in cart:
        return package_id.price * cart[package_id]


def get_cart_products(request):
    cats = Category.objects.all().order_by("-id")[:9]
    ids = list(request.session.get('cart').keys())
    cart_products = OfferManager.get_offer(ids)
    package_prices = list(map(map_function, cart_products))
    print(package_prices)
    total = sum(package_prices)

    args = {'cart_products': cart_products, 'total': total, "cats": cats}
    return render(request, 'buyingview/cart.html', args)


@login_required(login_url='user_login')
@has_selleraccount
def cartView(request):
    cats = Category.objects.all().order_by("-id")[:9]
    cart = request.session.get('cart', None)

    if request.method == "POST":
        cart = {}
        del request.session["cart"]
        return redirect("buying_view")

    # print(request.session.get("cart"))
    if not cart:
        request.session['cart'] = {}
    ids = list(request.session.get('cart').keys())
    cart_products = OfferManager.get_offer(ids)
    if cart is not None:
        if len(cart) > 1:
            cart_first_item = str(list(cart.keys())[0])
            cart_first_item_val = list(cart.values())[0]
            request.session['cart'] = {}
            request.session["cart"] = {cart_first_item: cart_first_item_val}
            ids = list(request.session.get('cart').keys())
            cart_products = OfferManager.get_offer(ids)
    # print(request.session.get("cart"))
    context = {
        'cart_products': cart_products,
        "cats": cats,
    }

    return render(request, 'buyingview/cart.html', context)


def create_checkout_random_slug(str_len):
    rand_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k = str_len))
    checkout = Checkout.objects.filter(slug=rand_slug)
    if checkout.exists():
        create_offer_random_slug(str_len)
    return rand_slug

@login_required(login_url='user_login')
@has_selleraccount
def checkout(request):
    cats = Category.objects.all().order_by("-id")[:9]
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    ids = list(request.session.get('cart').keys())
    cart_products = OfferManager.get_offer(ids)
    user = request.user
    print("EMAIL: " + user.email)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        due_date = request.POST.get('due_date')
        user = request.user
        # seller work

        packages = OfferManager.get_offer(list(cart.keys()))

        for package in packages:
            slug = create_checkout_random_slug(20)
            checkout = Checkout(
                slug=slug,
                first_name=first_name,
                last_name=last_name,
                address=address,
                due_date=due_date,
                user=user,
                package=package,
                price=package.price,
                quantity=cart.get(str(package.id)),
                seller = package.offer.user,
            )
            
            # checkout.order_status = ""
            
            checkout.save()
            
            rec = user.email
            email_subject = "Order Has been Placed Please Pay Now"
            email_message = render_to_string('mailview/order-complete.html', {
                
            })
            
            email = EmailMultiAlternatives(email_subject, email_message, to=[rec])
            email.attach_alternative(email_message, "text/html")
            email.send()
            
            request.session['cart'] = {}
            return redirect(f"/order_details/{checkout.id}/{checkout.slug}/")
            
            
            # send_mail(
            #     'Subject here',
            #     'USERNAME: ' + checkout.user.username + '\n'\
            #     'Thank you for ordering from Marketage. ' + '\n'\
            #     'Your order' + 'is now active. ' + '\n' \
            #     'You can review your order status at any time by visiting Your Account https://marketage.io/. \n'\

            #     'Your Order Id: ' + 'Marketage#' + str(checkout.id) + '\n' +
            #      'Package Name: ' + str(checkout.package) + '\n' \
            #      'Price: ' + str(checkout.price) + '\n' \
            #      'Quantity: ' + str(checkout.quantity) + '\n' \
            #      'Grand Total: ' + str(checkout.grand_total) + '\n'\
            #      '\n'\
            #      'We hope you enjoyed your shopping experience with us and that you will visit us again soon.' \
            #      '\n'\
            #      '\n'\
            #      'Copyright © 2021 Itna Global Ltd. All rights reserved.'\
            #      'IGL located at 2 Frederick Street, Kings Cross, London, United Kingdom, WC1X 0ND'\
            #      '\n'
            #      'Bangladesh Office Itna Global Limited, House 24, Road,1, Nikunja2, Dhaka 1229, Khilkhet, Phone  +8809613662222 Email itnaglobal@gmail.com',
                 
                
            #     'noreply.marketage@gmail.com',
            #     [checkout.user.email],
            #     # ['itna.sakib@gmail.com'],
            #     fail_silently=False,
            # )
            
            # return redirect('BuyerOrders')

    args = {
        'cart_products': cart_products,
        "cats": cats,
    }
    return render(request, 'buyingview/checkout.html', args)


# buyer order page views
@login_required(login_url='user_login')
@has_selleraccount
def get_buyer_orders_url(request):
    order_id = []
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    seller_submit = set()
    cats = Category.objects.all().order_by("-id")[:9]
    orders = Checkout.objects.filter(user=request.user).order_by("-id")
    
    not_delivered_orders = 0
    
    for item in orders:
        if item.order_status != "DELIVERED":
            not_delivered_orders += 1
    
    # onoing_projects = Checkout.objects.filter()
    premium_orders = PremiumOfferPackageCheckout.objects.filter(user=request.user).order_by('-id')
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    for order in orders:
        order_id.append(order.id)

    for item in SellerSubmit.objects.all().order_by("-id"):
        # print(item.checkout.id)
        if item.checkout.id in order_id:
            try:
                x = SellerSubmit.objects.filter(checkout=item.checkout.id).last()
            except:
                return redirect("BuyerOrders")
            else:
                seller_submit.add(x)
                
                
    ongoing_projects = 0
    
    for item in seller_submit:
        if item.checkout.order_status == "DELIVERED":
            ongoing_projects += 1

    # print(order_id)
    # print(seller_submit)
    
    order_seen = True
    
    # for item in seller_submit:
    #     if item.checkout.order_submitted_is_seen == False:
    #         item.checkout.order_submitted_is_seen = True
    #         item.checkout.save()
    
    unseen_orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    for item in unseen_orders:
        item.order_submitted_is_seen = True
        item.save()

    args = {
        "offers": offers,
        "not_delivered_orders": not_delivered_orders,
        "ongoing_projects": ongoing_projects,
        "orders": orders,
        "seller_submit": seller_submit,
        "premium_orders": premium_orders,
        "cats": cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "order_seen": order_seen,
        "all_seller_offers_seen": all_seller_offers_seen,
    }
    return render(request, 'buyingview/buying_orders.html', args)



# category wise Page Buying View
@login_required(login_url='user_login')
# @has_selleraccount
def category_wise_offers(request, slug):
    try:
        single_category = Category.objects.get(slug=slug)
    except Category.DoesNotExits:
        return redirect("buying_view")
        
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    cats = Category.objects.all().order_by("-id")[:9]
    category = Category.objects.all()
    catwise_offers = Offer.objects.filter(category__slug = slug, offer_status="ACTIVE")
    subcategory = Subcategory.objects.all()
    
    user_session = request.session.get("user", None)
    
    msg_seen_chatrooms = 0
    all_seller_offers_seen = True
    order_seen = True
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
 

    args = {
        "single_category": single_category,
        'catwise_offers': catwise_offers,
        'category': category,
        'cats': cats,
        'subcategory': subcategory,
        "offers": offers,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        }

    return render(request, 'landingview/category_wise_offers.html', args)


@login_required(login_url='user_login')
@has_selleraccount
def subcategory_wise_offers(request, slug):
    cats = Category.objects.all().order_by("-id")[:9]
    subcategory = Subcategory.objects.all()
    subcat = get_object_or_404(Subcategory, slug=slug)
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')

    sub_offers = Offer.objects.filter(sub_category__slug = slug, offer_status="ACTIVE")
    
    user_session = request.session.get("user", None)
    
    msg_seen_chatrooms = 0
    all_seller_offers_seen = True
    order_seen = True
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False

    args = {
        "subcat": subcat,
        "subcategory": subcategory,
        "sub_offers": sub_offers,
        "cats": cats,
        "offers": offers,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }
    return render(request, "landingview/subcategory_wise_offers.html", args)

@login_required(login_url='user_login')
@has_selleraccount
def added_post_request(request):
    if request.method == 'POST':
        user = request.user
        postrequest_title = request.POST.get("title")
        description = request.POST.get("description")
        attachment  = request.FILES.get("file_upload", None)
        category = request.POST.get("category")
        del_time = request.POST.get("del_time")
        price = request.POST.get("price")
        post_status = "ACTIVE"

        print("delivery time", del_time)
        print(user, postrequest_title, description, attachment, category, del_time, price)
        
        try:
            category = Category.objects.get(title=category)
            delivery_time = DeliveryTime.objects.get(title=del_time)
        except:
            return redirect("post_a_request")
        else:
            buyer_post = BuyerPostRequest(user=user, postrequest_title=postrequest_title,
                                            description=description, attachment=attachment,
                                            category=category, delivery_time=delivery_time,
                                            budget=price, post_status=post_status)
                                            
            buyer_post.save()
            
            buyer_post.seen_users.add(user)
                
            rec = user.email
            mail_subject = "YOUR REQUEST HAS BEEN POSTED"
            mail_message = render_to_string("mailview/post_a_request_email.html", {

            })
            email = EmailMultiAlternatives(mail_subject, mail_message, to=[rec])
            email.attach_alternative(mail_message, "text/html")
            email.send()
            
            return redirect("buyer-posts")
    else:
        return redirect("post_a_request")

@login_required(login_url='user_login')
@has_selleraccount
def post_a_request(request):
    cats = Category.objects.all().order_by("-id")[:9]
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    categories = Category.objects.all()
    delivery_time = DeliveryTime.objects.all()
    
    all_seller_offers_seen, order_seen = True, True
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    
    if len(orders) > 0:
        order_seen = False

    args = {
        'categories': categories,
        'delivery_time': delivery_time,
        "offers": offers,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, 'buyingview/post_request.html', args)


def get_become_a_seller_page(request):
    return render(request, 'landingview/become_a_seller.html')
    

# Order Details Page & SSLCOMMERZ
@login_required(login_url='user_login')
@has_selleraccount
def get_order_details_url(request, id, slug, *args, **kwargs):
    cats = Category.objects.all().order_by("-id")[:9]
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    
    try:
        order = Checkout.objects.get(pk=id, slug=slug)
        order.buyer_check = True
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        all_seller_offers_seen = True
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        order_seen = True
        
        if len(orders) > 0:
            order_seen = False
    # for sslcommerz
    except Checkout.DoesNotExist:
        return redirect("BuyerOrders")
    else:
        
        if request.method == "POST":
            settings = {
                'store_id': 'testbox', 'store_pass': 'qwerty', 'issandbox': True
            }
            user = request.user
            order = Checkout.objects.get(pk=id)
            print(order)
            first_name = order.first_name
            last_name = order.last_name
            address = order.address
            email = order.user.email
            phone_number = order.user.selleraccount.contact_no
            country = order.user.selleraccount.country
            # city = order.user.selleraccount.city
            package_category = order.package.offer.category
            quantity = order.quantity
            total = order.grand_total * 86 # CONVERTING USD TO BDT FOR SSLCOMMERZ
            transaction_id = order.id
    
            # Checkout.objects.filter(pk=kwargs['id'])
            Checkout.objects.filter(pk=id)
    
            sslcommerz = SSLCOMMERZ(settings)
            post_body = {}
            post_body['total_amount'] = total
            post_body['currency'] = "BDT"
            post_body['tran_id'] = transaction_id
            # post_body['tran_id'] = transaction_id
            post_body['success_url'] = "https://marketage.io/success/"
            post_body['fail_url'] = "https://marketage.io/failed/"
            post_body['cancel_url'] = "https://marketage.io/cancel/"
            post_body['emi_option'] = 0
            post_body['cus_name'] = first_name
            post_body['cus_email'] = email
            post_body['cus_add1'] = address
            post_body['cus_phone'] = phone_number
            post_body['cus_city'] = "N/A"
            post_body['cus_country'] = country
            post_body['shipping_method'] = "NO"
            post_body['multi_card_name'] = ""
            post_body['num_of_item'] = quantity
            post_body['product_name'] = order.package
            post_body['product_category'] = package_category
            post_body['product_profile'] = "general"
            print(post_body)
            response = sslcommerz.createSession(post_body)
            print(response)
            return redirect(response['GatewayPageURL'])
    args = {
        'order': order,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "offers": offers,
        "cats": cats,
    }

    return render(request, 'buyingview/order_details.html', args)


@csrf_exempt
def successView(request):
    if request.POST.get('status') == "VALID":
        tran_id = request.POST['tran_id']
        # print("TRAIN ID:", tran_id)
        order = Checkout.objects.get(id=tran_id)
        NotificationModel.objects.create(user=order.seller, content="You Have Received an order")
        order.paid = True
        order.is_checked = False
        order.buyer_check = True
        order.save()
        buyer = str(order.user)
        rec = str(order.seller.email)
        orderId = str(order.id)
        cut = order.total * 15 / 100
        total = order.total - cut
        mail_subject = "YOU GOT AN ORDER",
        message = render_to_string("mailview/seller_confirmation.html", {
                'rec': rec,
                'buyer': buyer,
                'orderId': orderId,
                'total': total,
            })
        email = EmailMultiAlternatives(mail_subject, message, to=[rec])
        email.attach_alternative(message, "text/html")
        try:
            email.send()
        except:
            return HttpResponse("ERROR 404!")
            
        # Sending to manager #
        mail_subject1 = "YOU HAVE ONE NEW NOTIFICATION",
        message1 = render_to_string("mailview/manager_notification.html", {
                'rec': rec,
                'buyer': buyer,
                'orderId': orderId,
                'total': total,
            })
        email1 = EmailMultiAlternatives(mail_subject1, message1, to=["notification@marketage.io"])
        email1.attach_alternative(message1, "text/html")
        try:
            email1.send()
        except:
            return HttpResponse("ERROR 404!")
        # email.send()
        
    return render(request, "responseview/success.html")


@login_required(login_url='user_login')
@has_selleraccount
@csrf_exempt
def failedView(request):
    return render(request, "responseview/failed.html")


@login_required(login_url='user_login')
@has_selleraccount
@csrf_exempt
def cancelledView(request):
    return render(request, "responseview/cancel.html")

@login_required(login_url='user_login')
def extendedUserView(request):
    cats = Category.objects.all().order_by("-id")[:9]
    countries = Country.objects.all()
    
    user_session = request.session.get("user", None)

    if user_session is not None:
        seller_account = SellerAccount.objects.filter(user=request.user)
        
        if seller_account.exists():
            return redirect("buying_view")
        if request.method == "POST":
            contact_no = request.POST.get("contact_no")
            profile_picture = request.FILES.get("profile_picture")
            country_id = request.POST.get("country")
            # print(request.user, email, contact_no, profile_picture, country_id)
            try:
                country = Country.objects.get(id=country_id)

                if not contact_no and not profile_picture:
                    return redirect("extended-user")
            except:
                return redirect("extended-user")
            else:
                SellerAccount.objects.create(user=request.user,
                                             contact_no=contact_no, profile_picture=profile_picture,
                                             country=country)
                return redirect('buying_view')
    else:
        return redirect("user_registration")

    args = {
        "countries": countries,
        "cats": cats,
    }
    return render(request, "wasekPart/extendedForm.html", args)


@login_required(login_url='user_login')
@has_selleraccount
def sellerSubmitView(request, pk, slug):
    cats = Category.objects.all().order_by("-id")[:9]
    check = Checkout.objects.filter(id=pk, slug=slug).last()
    check.is_checked = True
    check.save()
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
        
    # print(pk)
    if request.method == "POST":
        file_field = request.FILES.get("file_field")
        
        if file_field is None:
            return redirect(f"/seller-submit/{pk}/{slug}/")
        
        try:
            checkout = Checkout.objects.get(id=pk, slug=slug)
        except:
            return redirect("manage-order")
        else:
            SellerSubmit.objects.create(
                checkout=checkout, file_field=file_field
            )

            checkout.order_status = "DELIVERED"
            checkout.is_submitted = True
            checkout.order_submitted_is_seen = False
            checkout.save()


            # Email Sending #
            buyer = checkout.user.email
            seller = checkout.seller
            seller_email = checkout.seller.email
            orderId = checkout.id
            email_subject = "ORDER HAS BEEN DELIVERED"
            stat = checkout.order_status
            message = render_to_string("mailview/seller_submit_to_buyer.html", {
                "buyer": buyer,
                "stat": stat,
                "seller": seller,
                "orderId": orderId
            })
            email = EmailMultiAlternatives(email_subject, message, to=[buyer])
            email.attach_alternative(message, "text/html")
            email.send()


            email_subject2 = "YOU ORDER HAS BEEN DELIVERED TO BUYER"
            mail_msg = render_to_string("mailview/seller_order_deliver.html", {

            })
            email2 = EmailMultiAlternatives(email_subject2, mail_msg, to=[seller_email])
            email2.attach_alternative(mail_msg, "text/html")
            email2.send()


            return redirect("manage-order")

    args = {
        "checkout_id": pk,
        "seller_sees_order": seller_sees_order,
        "cats": cats,
    }
    return render(request, "wasekPart/sellerSubmit.html", args)



# Testing Purpose

def all_test_orders(request):
    cats = Category.objects.all().order_by("-id")[:9]
    orders = Checkout.objects.filter(is_complete=True)

    args = {
        "orders": orders,
        "cats": cats,
    }

    return render(request, "testpart/order_test.html", args)


# Review Sellers
@login_required(login_url='user_login')
@has_selleraccount
def reviewSellerForm(request, username):
    seller = User.objects.get(username=username)
    cats = Category.objects.all().order_by("-id")[:9]

    if request.method == 'POST':
        pass

    args = {
        "seller": seller,
        "cats": cats,
    }
    return render(request, "testpart/test2.html", args)





# Rating Sellers


# Top Offers


## Footer Part ---------- >>>>>


@login_required(login_url='user_login')
def aboutusView(request):
    user_session = request.session.get("user", None)
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    all_seller_offers_seen = True
    order_seen = True
    
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, "azimpart/aboutus.html", args)


@login_required(login_url='user_login')
def privacypolicyView(request):
    user_session = request.session.get("user", None)
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    all_seller_offers_seen = True
    order_seen = True
    
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, "azimpart/privacy-policy.html", args)

@login_required(login_url='user_login')
@has_selleraccount
def helpSupportView(request):
    cats = Category.objects.all().order_by("-id")[:9]
    support_category = SupportCategoryModel.objects.all()
    # print("SUPPORTTTT" + str(support_category))
    # print("18231298312938172938127")
    
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False

    if request.method=='POST':
        user = request.user
        email = request.POST.get('email')
        subject = request.POST.get('subject')    
        attachment = request.FILES.get('attachment')
        image_attachment = request.FILES.get('image_attachment')
        description = request.POST.get('description')

        subject = SupportCategoryModel.objects.get(title=subject)

        saved = SupportModel(
            user = user,
            email = email,
            subject = subject,
            attachment = attachment,
            image_attachment = image_attachment,
            description = description,
            support_ticket = uuid.uuid4().hex[:6].upper()
        )
        # print(saved)
        saved.support_status = "PENDING"
        saved.save()
        support_ticket = saved.support_ticket
        email_subject = "Support Ticket has been created"
        email_message = render_to_string('mailview/suport_ticket', {
            "support_ticket": support_ticket
        })
            
        email = EmailMultiAlternatives(email_subject, email_message, to=[rec])
        email.attach_alternative(email_message, "text/html")
        email.send()
        
        
        
        # send_mail(
        #         'SUPPORT TICKET CREATED',
        #         'USERNAME: ' + saved.user.username + '\n'\
        #         'You Support ticket has been created successfully' + '\n' \
        #             'You Ticket No.' + saved.support_ticket + '\n' \
        #         'For getting reply you will have to wait 24 hours at least'+'\n' \
        #          'Copyright © 2021 Itna Global Ltd. All rights reserved.'\
        #          'IGL located at 2 Frederick Street, Kings Cross, London, United Kingdom, WC1X 0ND'\
        #          '\n'
        #          'Bangladesh Office Itna Global Limited, House 24, Road,1, Nikunja2, Dhaka 1229, Khilkhet, Phone  +8809613662222 Email itnaglobal@gmail.com',
                 
                
        #         'noreply.marketage@gmail.com',
        #         [email],
        #         fail_silently=False,
        #     )
        return redirect('buying_view')
    args = {
        'support_category': support_category,
        'cats': cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "order_seen": order_seen,
        "all_seller_offers_seen": all_seller_offers_seen,
    }
    return render(request, "azimpart/help-support.html", args)


@login_required(login_url='user_login')
def trustSafetyView(request):
    user_session = request.session.get("user", None)
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    all_seller_offers_seen = True
    order_seen = True
    
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, "azimpart/trust-safety.html", args)


@login_required(login_url='user_login')
def termOfservicesView(request):
    user_session = request.session.get("user", None)
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    all_seller_offers_seen = True
    order_seen = True
    
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, "azimpart/term-services.html", args)


## Footer Aprt ENd ------->>>


def create_offer_random_slug(str_len):
    rand_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k = str_len))
    offer = Offer.objects.filter(slug=rand_slug)
    if offer.exists():
        create_offer_random_slug(str_len)
    return rand_slug


def create_offer_random_slug(str_len):
    rand_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k = str_len))
    offer = Offer.objects.filter(slug=rand_slug)
    if offer.exists():
        create_offer_random_slug(str_len)
    return rand_slug


@login_required(login_url='user_login')
@has_selleraccount
def createOfferView(request):
    offer = Offer.objects.filter(user=request.user)
    cats = Category.objects.all().order_by("-id")[:9]
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if (len(offer) > 7):
        return redirect("manage-offers")
        
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
        
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    child_cats = ChildSubcategory.objects.all()
    services = Services.objects.all()
    deliveries = DeliveryTime.objects.all()
    revisions = Revision.objects.all()
    num_of_pages = NumberOfPage.objects.all()

    if request.method == "POST":
        # Creating random slug
        slug = create_offer_random_slug(20)

        offer_title = request.POST.get("offer_title")
        seo_title = request.POST.get("seo_title")
        category = request.POST.get("category")
        service = request.POST.get("service")
        basic_shortDesc = request.POST.get("basic_shortDesc")
        standard_shortDesc = request.POST.get("standard_shortDesc")
        premium_shortDesc = request.POST.get("premium_shortDesc")
        delivery_time_basic = request.POST.get("delivery_time_basic")
        delivery_time_standard = request.POST.get("delivery_time_standard")
        delivery_time_premium = request.POST.get("delivery_time_premium")
        num_pages_basic = request.POST.get("num_pages_basic")
        num_pages_standard = request.POST.get("num_pages_standard")
        num_pages_premium = request.POST.get("num_pages_premium")
        is_responsive_basic = request.POST.get("is_responsive_basic")
        is_responsive_standard = request.POST.get("is_responsive_standard")
        is_responsive_premium = request.POST.get("is_responsive_premium")
        revision_basic = request.POST.get("revision_basic")
        revision_standard = request.POST.get("revision_standard")
        revision_premium = request.POST.get("revision_premium")
        price_basic = request.POST.get("price_basic")
        price_standard = request.POST.get("price_standard")
        price_premium = request.POST.get("price_premium")
        content = request.POST.get("content")
        main_image = request.FILES.get("offer_main_image")
        uploaded_photo = request.FILES.getlist("uploaded_photo")
        uploaded_video = request.FILES.get("uploaded_video")
        document = request.FILES.get("document")
        child_cat = request.POST.get("child_cat")
        subcategory = request.POST.get("subcategory")
        
        try:
            category = Category.objects.get(title=category)
            subcategory = Subcategory.objects.get(sub_title=subcategory)
            child_cat = ChildSubcategory.objects.get(child_title=child_cat)
            service = Services.objects.get(title=service)
        except:
            return redirect("create-offer")
        else:
        # Creating offer object

        # if main_image and uploaded_video and document:
        #     offer = Offer(slug=slug, user=request.user, offer_title=offer_title, seo_title=seo_title, 
        #                 image=main_image, offer_video=uploaded_video, document=document, 
        #                 service=service, category=category, description=content)
        #     offer.save()
            if main_image:
                offer = Offer(slug=slug, user=request.user, offer_title=offer_title, seo_title=seo_title, image=main_image,
                    service=service, child_subcategory=child_cat, category=category, sub_category=subcategory, description=content)
                if uploaded_video:
                    offer.offer_video = uploaded_video
                if document:
                    offer.document = document
                    
                offer.save()
            
            if len(uploaded_photo) > 0:
                for item in uploaded_photo[:3]:
                    image_obj = ExtraImage(image=item)
                    image_obj.save()
                    offer.extra_images.add(image_obj.id)
    
            if basic_shortDesc is not None:
                try:
                    dt_basic = DeliveryTime.objects.get(title=delivery_time_basic)
                    re_basic = Revision.objects.get(title=revision_basic)
                    
                    num_page_basic = None
                    if num_pages_basic:
                        num_page_basic = NumberOfPage.objects.get(title=num_pages_basic)
                except:
                    offer.delete()
                    return redirect("create-offer")
                # print(num_page_basic)
                else:
                    if is_responsive_basic == "on":
                        is_responsive_basic = True
                    else:
                        is_responsive_basic = False
    
                    # Saving Package
                    if num_page_basic is not None:
                        package = Package(title="Basic", delivery_time=dt_basic, package_desc=basic_shortDesc, 
                                        revision_basic=re_basic, num_of_pages_for_basic=num_page_basic, is_responsive_basic=is_responsive_basic,
                                        )
                    else:
                        package = Package(title="Basic", delivery_time=dt_basic, package_desc=basic_shortDesc, 
                                        revision_basic=re_basic, is_responsive_basic=is_responsive_basic,
                                        )
                    package.save()
                    OfferManager.objects.create(offer=offer, package=package, price=price_basic)
    
            if standard_shortDesc is not None:
                try:
                    dt_standard = DeliveryTime.objects.get(title=delivery_time_standard)
                    re_standard = Revision.objects.get(title=revision_standard)
                    num_page_standard = None
                    if num_pages_standard:
                        num_page_standard = NumberOfPage.objects.get(title=num_pages_standard)
                # print(num_page_standard)
                except:
                    offer.delete()
                    return redirect("create-offer")
                else:
                    if is_responsive_standard == "on":
                        is_responsive_standard = True
                    else:
                        is_responsive_standard = False
                    
                    if num_page_standard is not None:
                        package = Package(title="Standard", delivery_time=dt_standard, package_desc=standard_shortDesc, 
                                        revision_standard=re_standard, num_of_pages_for_standard=num_page_standard, is_responsive_standard=is_responsive_standard,
                                        )
                    else:
                        package = Package(title="Standard", delivery_time=dt_standard, package_desc=standard_shortDesc, 
                                        revision_standard=re_standard, is_responsive_standard=is_responsive_standard,
                                        )
                    package.save()
                    OfferManager.objects.create(offer=offer, package=package, price=price_standard)
    
            if premium_shortDesc is not None:
                try:
                    dt_premium = DeliveryTime.objects.get(title=delivery_time_premium)
                    re_premium = Revision.objects.get(title=revision_premium)
                    num_page_premium = None
                    if num_pages_premium:
                        num_page_premium = NumberOfPage.objects.get(title=num_pages_premium)
                # print(num_page_premium)
                except:
                    offer.delete()
                    return redirect("create-offer")
                else:
                    if is_responsive_premium == "on":
                        is_responsive_premium = True
                    else:
                        is_responsive_premium = False
    
                    # Creating package object

                    if num_page_premium is not None:
                        package = Package(title="Premium", delivery_time=dt_premium, package_desc=premium_shortDesc, 
                                        revision_premium=re_premium, num_of_pages_for_premium=num_page_premium, is_responsive_premium=is_responsive_premium,
                                        )
                    else:
                        print("PREMIUM NOT FOUND!")
                        package = Package(title="Premium", delivery_time=dt_premium, package_desc=premium_shortDesc, 
                                        revision_premium=re_premium, is_responsive_premium=is_responsive_premium,
                                        )
                    package.save()
                    # Creating offer manager object
                    OfferManager.objects.create(offer=offer, package=package, price=price_premium)
    
            return redirect("manage-offers")
    args = {
        "cats": cats,
        "categories": categories,
        "subcategories": subcategories,
        "child_cats": child_cats,
        "services": services,
        "deliveries": deliveries,
        "revisions": revisions,
        "num_of_pages": num_of_pages,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }
    return render(request, "sellingview/create_offer.html", args)

@login_required(login_url='user_login')
@has_selleraccount
def edit_offer(request, id, slug):
    cats = Category.objects.all().order_by("-id")[:9]
    basic_package, standard_package, premium_package = None, None, None
    basic_deliveries, standard_deliveries, premium_deliveries = None, None, None
    basic_num_pages, standard_num_pages, premium_num_pages = None, None, None
    basic_revisions, standard_revisions, premium_revisions = None, None, None
    basic_price, standard_price, premium_price = None, None, None
    document = None, 
    offer_first_img, offer_second_img, offer_third_img = None, None, None
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)

    try:
        offer = Offer.objects.get(id=id, slug=slug)
    except Offer.DoesNotExist:
        return redirect("manage-offers")
    else:
        categories = Category.objects.exclude(title=offer.category.title)
        subcategories = Subcategory.objects.exclude(sub_title=offer.sub_category.sub_title)
        child_cats = ChildSubcategory.objects.exclude(child_title=offer.child_subcategory.child_title)
        services = Services.objects.exclude(title=offer.service.title)
        offermanager = OfferManager.objects.filter(offer=offer)
        document = str(offer.document).split("/")[-1]
        if len(offer.extra_images.all()) > 0:
            for i, item in enumerate(offer.extra_images.all()):
                if i == 0:
                    offer_first_img = item
                elif i == 1:
                    offer_second_img = item
                elif i == 2:
                    offer_third_img = item

        # print(document)

        if offermanager.exists():
            for i, item, in enumerate(offermanager):
                # Basic package
                if i == 0:
                    basic_package = item.package
                    basic_deliveries = DeliveryTime.objects.exclude(title=basic_package.delivery_time.title)
                    if basic_package.num_of_pages_for_basic:
                        basic_num_pages = NumberOfPage.objects.exclude(title=basic_package.num_of_pages_for_basic.title)
                    else:
                        basic_num_pages = NumberOfPage.objects.all()
                    basic_revisions = Revision.objects.exclude(title=basic_package.revision_basic.title)
                    basic_price = item.price
                # Standard package
                elif i == 1:
                    standard_package = item.package
                    standard_deliveries = DeliveryTime.objects.exclude(title=standard_package.delivery_time.title)
                    if standard_package.num_of_pages_for_standard:
                        standard_num_pages = NumberOfPage.objects.exclude(title=standard_package.num_of_pages_for_standard.title)
                    else:
                        standard_num_pages = NumberOfPage.objects.all()
                    standard_revisions = Revision.objects.exclude(title=standard_package.revision_standard.title)
                    standard_price = item.price
                # Premium package
                elif i == 2:
                    premium_package = item.package
                    premium_deliveries = DeliveryTime.objects.exclude(title=premium_package.delivery_time.title)
                    if premium_package.num_of_pages_for_premium:
                        premium_num_pages = NumberOfPage.objects.exclude(title=premium_package.num_of_pages_for_premium.title)
                    else:
                        premium_num_pages = NumberOfPage.objects.all()
                    premium_revisions = Revision.objects.exclude(title=premium_package.revision_premium.title)
                    premium_price = item.price
    
        # print(basic_package, standard_package, premium_package)

        if request.method == "POST":
            main_image_id = request.POST.get("main_image_id", None)
            extra_image_id1 = request.POST.get("extra_image_id1", None)
            extra_image_id2 = request.POST.get("extra_image_id2", None)
            extra_image_id3 = request.POST.get("extra_image_id3", None)
            offer_video_id = request.POST.get("offer_video_id", None)
            offer_document_id = request.POST.get("offer_document_id", None)
            offer_title = request.POST.get("offer_title")
            seo_title = request.POST.get("seo_title")
            category = request.POST.get("category")
            subcategory = request.POST.get("subcatgory")
            child_subcat = request.POST.get("child_subcat")
            service = request.POST.get("service")
            basic_shortDesc = request.POST.get("basic_shortDesc")
            standard_shortDesc = request.POST.get("standard_shortDesc")
            premium_shortDesc = request.POST.get("premium_shortDesc")
            delivery_time_basic = request.POST.get("delivery_time_basic")
            delivery_time_standard = request.POST.get("delivery_time_standard")
            delivery_time_premium = request.POST.get("delivery_time_premium")
            num_page_basic = request.POST.get("num_pages_basic")
            num_page_standard = request.POST.get("num_pages_standard")
            num_page_premium = request.POST.get("num_pages_premium")
            basic_responsive = request.POST.get("is_responsive_basic")
            standard_responsive = request.POST.get("is_responsive_standard")
            premium_responsive = request.POST.get("is_responsive_premium")
            revision_basic = request.POST.get("revision_basic")
            revision_standard = request.POST.get("revision_standard")
            revision_premium = request.POST.get("revision_premimum")
            price_basic = request.POST.get("price_basic")
            price_standard = request.POST.get("price_standard")
            price_premium = request.POST.get("price_premium")
            content = request.POST.get("content")
            offer_mainImage = request.FILES.get("offer_main_image")
            offer_extraImages = request.FILES.getlist("offer_extraImages")
            offer_video = request.FILES.get("offer_video")
            offer_document = request.FILES.get("offer_document")

            # print("OFFER EXTRA IMAGES:")
            # print(offer_extraImages)

            # Deleting offer main image
            if main_image_id:
                offer.image = None
                offer.offer_status = "PAUSED"

            # Deleting an extra image from offer
            if extra_image_id1:
                offer.extra_images.remove(int(offer_first_img.id))
                # offer.offer_status = "PAUSED"
            elif extra_image_id2:
                offer.extra_images.remove(int(offer_second_img.id))
                # offer.offer_status = "PAUSED"
            elif extra_image_id3:
                offer.extra_images.remove(int(offer_third_img.id))
                # offer.offer_status = "PAUSED"

            # Deleting offer video
            if offer_video_id:
                offer.offer_video = None
                # offer.offer_status = "PAUSED"

            # Deleting offer document
            if offer_document_id:
                offer.document = None
                # offer.offer_status = "PAUSED"
            
            try:
                service = Services.objects.get(title=service)
                category = Category.objects.get(title=category)
                subcategory = Subcategory.objects.get(sub_title=subcategory)
                child_subcat = ChildSubcategory.objects.get(child_title=child_subcat)
            except:
                return redirect(f"/edit_offer/{offer.id}/{offer.slug}/")
            else:
                offer.offer_title = offer_title
                offer.seo_title = seo_title
    
                if offer_mainImage:
                    offer.image = offer_mainImage
                if offer_video:
                    offer.offer_video = offer_video
                if offer_document:
                    offer.document = offer_document
    
                # print("OFFER EXTRA IMAGE LENGTH:", len(offer.extra_images.all()))
    
                # if offer.image != None and offer.offer_video != None and offer.document != None and len(offer.extra_images.all()) > 0:
                #     offer.offer_status = "ACTIVE"
                    
                if offer.image != None and offer.offer_status == "PENDING APPROVAL":
                    offer.offer_status = "PENDING APPROVAL"
                elif offer.image != None and offer.offer_status == "ACTIVE":
                    offer.offer_status = "ACTIVE"
                elif offer.image != None and offer.offer_status == "PAUSED" and offer.is_pending == False:
                    offer.offer_status = "ACTIVE"
                elif offer.image != None and offer.offer_status == "PAUSED" and offer.is_pending == True:
                    offer.offer_status = "PENDING APPROVAL"
                    
    
                offer.service = service
                offer.category = category
                offer.sub_category = subcategory
                offer.child_subcategory = child_subcat
                offer.description = content
    
                offer.save()
                
                if main_image_id or extra_image_id1 or extra_image_id2 or extra_image_id3 or offer_video_id or offer_document_id:
                    return redirect(f"/edit_offer/{offer.id}/{offer.slug}/")
                
                # Adding offer extra images
                if offer_extraImages:
                    for item in offer_extraImages[:3-len(offer.extra_images.all())]:
                        image_obj = ExtraImage(image=item)
                        image_obj.save()
                        offer.extra_images.add(image_obj.id)
                
                for i, item, in enumerate(offermanager):
                    # Basic package
                    if i == 0:
                        item.package.package_desc = basic_shortDesc
                        revision_basic = Revision.objects.get(title=revision_basic)
                        delivery_time_basic = DeliveryTime.objects.get(title=delivery_time_basic)
                        item.package.revision_basic = revision_basic
                        item.package.delivery_time = delivery_time_basic
                        num_pages_basic = None


                        if category.title == "Programming & Tech":
                            if num_page_basic:
                                num_pages_basic = NumberOfPage.objects.get(title=num_page_basic)
                            if num_pages_basic is not None:
                                item.package.num_of_pages_for_basic = num_pages_basic
                        else:
                            item.package.num_of_pages_for_basic = num_pages_basic
                        
                        if basic_responsive == "on":
                            is_basic_responsive = True
                        else:
                            is_basic_responsive = False
    
                        item.package.is_responsive_basic = is_basic_responsive
                        item.price = price_basic
                        item.package.save()
                        item.save()
                    # Standard package
                    elif i == 1:
                        item.package.package_desc = standard_shortDesc
                        revision_standard = Revision.objects.get(title=revision_standard)
                        delivery_time_standard = DeliveryTime.objects.get(title=delivery_time_standard)
                        item.package.revision_standard = revision_standard
                        item.package.delivery_time = delivery_time_standard
                        num_pages_standard = None

                        if category.title == "Programming & Tech":
                            if num_page_standard:
                                num_pages_standard = NumberOfPage.objects.get(title=num_page_standard)
                            if num_pages_standard is not None:
                                item.package.num_of_pages_for_standard = num_pages_standard
                        else:
                            item.package.num_of_pages_for_standard = num_pages_standard
                        
                        if standard_responsive == "on":
                            is_standard_responsive = True
                        else:
                            is_standard_responsive = False
    
                        item.package.is_responsive_standard = is_standard_responsive
                        item.price = price_standard
                        item.package.save()
                        item.save()
                    # Premium package
                    elif i == 2:
                        item.package.package_desc = premium_shortDesc
                        revision_premium = Revision.objects.get(title=revision_premium)
                        delivery_time_premium = DeliveryTime.objects.get(title=delivery_time_premium)
                        item.package.revision_premium = revision_premium
                        item.package.delivery_time = delivery_time_premium
                        num_pages_premium = None

                        if category.title == "Programming & Tech":
                            if num_page_premium:
                                num_pages_premium = NumberOfPage.objects.get(title=num_page_premium)
                            if num_pages_premium is not None:
                                item.package.num_of_pages_for_premium = num_pages_premium
                        else:
                            item.package.num_of_pages_for_premium = num_pages_premium
                        
                        if premium_responsive == "on":
                            is_premium_responsive = True
                        else:
                            is_premium_responsive = False
    
                        item.package.is_responsive_premium = is_premium_responsive
                        item.price = price_premium
                        item.package.save()
                        item.save()
    
                # return redirect(f"/edit_offer/{offer.id}/")
                return redirect("manage-offers")

    args = {
        "cats": cats,
        "offer": offer,
        "categories": categories,
        "subcategories": subcategories,
        "child_cats": child_cats,
        "services": services,
        "basic_package": basic_package,
        "standard_package": standard_package,
        "premium_package": premium_package,
        "basic_deliveries": basic_deliveries,
        "standard_deliveries": standard_deliveries,
        "premium_deliveries": premium_deliveries,
        "basic_num_pages": basic_num_pages,
        "standard_num_pages": standard_num_pages,
        "premium_num_pages": premium_num_pages,
        "basic_revisions": basic_revisions,
        "standard_revisions": standard_revisions,
        "premium_revisions": premium_revisions,
        "basic_price": basic_price,
        "standard_price": standard_price,
        "premium_price": premium_price,
        "document": document,
        "offer_first_img": offer_first_img,
        "offer_second_img": offer_second_img,
        "offer_third_img": offer_third_img,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }
    return render(request, 'azimpart/edit_offer.html', args)


@login_required(login_url='user_login')
@has_selleraccount
def seller_order_details(request, id):
    cats = Category.objects.all().order_by("-id")[:9]
    order = Checkout.objects.get(pk=id)
    today_date = date.today()
    duration = str(order.due_date - today_date).split(",")[0]
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)

    # print(duration)
    # print(type(duration))
    
    args = {
        'order': order,
        "duration": duration,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "cats": cats,
    }
    return render(request, 'sellingview/seller_order_details.html', args)



 ###################### 1 ALGO HERE #############################################
@login_required(login_url='user_login')
@has_selleraccount
def buyerOfferFormView(request, pk, slug):
    seller_submit = None
    cats = Category.objects.all().order_by("-id")[:9]
    
    try:
        order = Checkout.objects.get(id=pk, slug=slug)
        
        order.order_submitted_is_seen = True
        order.save()
        
        seller_submit = SellerSubmit.objects.filter(checkout=order)
        if seller_submit.exists():
            seller_submit = seller_submit.last()
    except:
        messages.error(request, "Error while submitting!")
    else:
        if request.method == "POST":
            order_status = request.POST.get("order_status")

            l = Checkout.objects.filter(is_complete=True).filter(
                 seller=request.user).count()
            # print(l)
            cancel_amount = Checkout.objects.filter(is_cancel=True).filter(
                seller=request.user
            ).count()

            calc = order.total * 20 / 100
            amount = order.total - calc
            # print("MY AMOUNT" + str(amount))
            
            # Wallet add system web hooks
            seller_wallet = order.seller.selleraccount.wallet
            if order_status == "complete" and l <= 15:
                order.order_status = "COMPLETED"
                order.is_complete = True
                order.is_cancel = False
                order.on_review = False
                order.seller.selleraccount.wallet += amount
                order.seller.selleraccount.point += 10
                print(order.seller.selleraccount.point)
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")

            elif order_status == "complete" and l > 15:
                order.order_status = "COMPLETED"
                order.is_complete = True
                order.is_cancel = False
                order.on_review = False
                order.seller.selleraccount.level = 1
                order.seller.selleraccount.wallet += amount
                order.seller.selleraccount.point += 15
                order.seller.selleraccount.is_new = False
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "complete" and l > 25:
                order.order_status = "COMPLETED"
                order.is_complete = True
                order.is_cancel = False
                order.on_review = False
                order.seller.selleraccount.level += 1
                order.seller.selleraccount.wallet += amount
                order.seller.selleraccount.point += 30
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "complete" and l > 35:
                order.order_status = "COMPLETED"
                order.order_status = True
                order.is_cancel = False
                order.on_review = False
                order.seller.selleraccount.level += 1
                order.seller.selleraccount.wallet += amount
                order.seller.selleraccount.point += 50
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "complete" and l > 50:
                order.order_status = "COMPLETED"
                order.order_status = True
                order.is_cancel = False
                order.on_review = False
                order.seller.selleraccount.level += 1
                order.seller.selleraccount.wallet += amount
                order.seller.selleraccount.point += 100
                order.seller.selleraccount.is_professional = True
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")

            # Leveling Down ALgorithm
            
            elif order_status == "cancel" and cancel_amount <= 5:
                order.order_status = "CANCELLED"
                order.is_cancel = True
                order.is_complete = False
                order.is_review = False
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
                
            elif order_status == "cancel" and cancel_amount > 5:
                order.order_status = "CANCELLED"
                order.is_cancel = True
                order.is_complete = False
                order.is_review = False
                order.seller.selleraccount.level -= 1
                order.seller.selleraccount.point -= 10
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "cancel" and cancel_amount > 10:
                order.order_status = "CANCELLED"
                order.is_cancel = True
                order.is_complete = False
                order.is_review = False
                order.seller.selleraccount.level -= 1
                order.seller.selleraccount.point -= 10
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "cancel" and cancel_amount > 12:
                order.order_status == "CANCELLED"
                order.is_cancel = True
                order.is_complete = False
                order.is_review = False
                order.seller.selleraccount.level -= 1
                order.seller.selleraccount.point -= 10
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "cancel" and cancel_amount > 15:
                order.order_status == "CANCELLED"
                order.is_cancel = True
                order.is_complete = False
                order.is_review = False
                order.seller.selleraccount.level -= 1
                order.seller.selleraccount.point -= 10
                order.seller.selleraccount.is_ban = True
                order.seller.selleraccount.save()
                order.order_is_seen = False
                order.save()
                return redirect("BuyerOrders")
            
            elif order_status == "review":
                rec = order.seller.email
                order.order_status = "ON REVIEW"
                order.on_review = True
                order.is_complete = False
                order.is_cancel = False
                order.order_is_seen = False
                send_notification = NotificationModel(
                    user=order.seller,
                    orderId=order,
                    content="Your Order is in review! Please check"
                )
                send_notification.save()
                order.save()

                # Sending Email to Seller
                client = order.user
                email_subject = "YOUR ORDER IS ON REVIEW!"
                email_message = render_to_string("mailview/order_on_review.html", {
                    'rec': rec,
                    'client': client,
                })
                email = EmailMultiAlternatives(email_subject, email_message, to=[rec])
                email.attach_alternative(email_message, "text/html")
                email.send()
                
                return redirect("BuyerOrders")
            else:
                messages.error(request, "Error while submitting!")
    # seller_submit = SellerSubmit.objects.get(checkout=order)
    args = {
        "seller_submit": seller_submit,
        "order": order,
        "cats": cats,
    }
    return render(request, "wasekPart/buyer_gigForm.html", args)
################################################## ALGO PART ENDS HERE ###############################################################





@login_required(login_url='user_login')
@has_selleraccount
def buyerDashboardFormView(request):
    orders = Checkout.objects.filter(
        user=request.user, order_status="DELIVERED", is_complete=False).order_by("-id")
    cats = Category.objects.all().order_by("-id")[:9]

    args = {
        "orders": orders,
        "cats": cats,
    }

    return render(request, "wasekPart/buyer_dashboard.html", args)

# Download Function
@login_required(login_url='user_login')
# @has_selleraccount
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as fh:
            response = HttpResponse(
                fh.read(), content_type="application/file_field")
            response["Content-Disposition"] = "inline;filename=" + \
                os.path.basename(file_path)
            return response
    raise Http404
    
@login_required(login_url='user_login')
@has_selleraccount
def searchPageView(request, *args, **kwargs):
    if request.method == 'GET':
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
        cats = Category.objects.all().order_by("-id")[:9]
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        all_seller_offers_seen = True
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        order_seen = True
        
        if len(orders) > 0:
            order_seen = False
        
        categories = Category.objects.all()
        search = request.GET.get('search')
        
        if search.strip() == "":
            return redirect("buying_view")
        
        results = Offer.objects.filter(seo_title__icontains=search, offer_status="ACTIVE")
        args = {
                'search': search,
                'results': results,
                'categories': categories,
                "offers": offers,
                "cats": cats,
                "order_seen": order_seen,
                "all_seller_offers_seen": all_seller_offers_seen,
                "msg_seen_chatrooms": msg_seen_chatrooms,
                }
        return render(request, "buyingview/search-box-Result.html", args)
    else:
        return redirect("page-404")


@login_required(login_url='user_login')
@has_selleraccount
def buyer_requestView(request):
    cats = Category.objects.all().order_by("-id")[:9]
    submitted_offer, active_posts = [], None
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    post_seen = True
    
    excluded_buyer_posts = BuyerPostRequest.objects.exclude(seen_users=request.user)
        
    for item in excluded_buyer_posts:
        item.seen_users.add(request.user)

    if request.user:
        # all_buyer_posts = BuyerPostRequest.objects.all()
        # all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
        
        
        active_post_requests = BuyerPostRequest.objects.filter(post_status="ACTIVE").order_by("-id").exclude(user=request.user)
        send_offer_requests = SendOfferModel.objects.filter(seller=request.user).order_by("-id")

        for x in active_post_requests:
            for y in send_offer_requests:
                print(x.postrequest_title, y.buyer_post_request)
                if str(x.postrequest_title) == str(y.buyer_post_request):
                    submitted_offer.append(x.postrequest_title)
        
        # print("SUBMITTED OFFER:", submitted_offer)
        
        if len(submitted_offer) > 0:
            for item in submitted_offer:
                active_post_requests = active_post_requests.exclude(postrequest_title=item)
                
        
    else:
        return redirect("user_login")

    args = {
        "active_post_requests": active_post_requests,
        "send_offer_requests": send_offer_requests,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "cats": cats,
    }
    return render(request, "azimpart/buyer_request.html", args)


def my_contacts_page(request):
    return render(request, "azimpart/my_contacts.html")



# User Details
@login_required(login_url='user_login')
@has_selleraccount
def account_detailsView(request, user_id, user_username):
    cats = Category.objects.all().order_by("-id")[:9]
    user_details = User.objects.get(pk=user_id, username=user_username)
    offers = Offer.objects.filter(user=user_id)
    
    # if user_details.username != request.user and user_details.id != user_id:
    #     return redirect("buying_view")
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True

    reviews = ReviewSeller.objects.filter(seller=user_details)
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_image")
        seller_account = get_object_or_404(SellerAccount, user=request.user)
        if profile_pic:
            seller_account.profile_picture = profile_pic
            seller_account.save()
    
    args = {
        'user_details': user_details,
        'offers': offers,
        "post_seen": post_seen,
        "reviews": reviews,
        "seller_sees_order": seller_sees_order,
        "cats": cats,
    }

    return render(request, 'sellingview/account.html', args)





@login_required(login_url='user_login')
@has_selleraccount
def earnings(request, id):
    cats = Category.objects.all().order_by("-id")[:9]
    if id != request.user.id:
        return redirect("buying_view")
    
    user = request.user
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if user is not None:
        seller_details = User.objects.get(pk=id)

        # orders_by_seller = Checkout.objects.filter(
        #     Q(seller = request.user) & Q(is_complete=True)
        # ).order_by('-created_at')
        
        orders_by_seller = Checkout.objects.filter(
            seller=request.user, is_complete=True
        ).order_by('-created_at')
        
        

        balance = seller_details.selleraccount.wallet
        
        total_withdraw_amount = 0
        
        withdraw_obj = WithDrawModel.objects.filter(user=request.user, stat="CLEARED")
        
        if withdraw_obj:
            for item in withdraw_obj:
                total_withdraw_amount += item.amount
                
        availabel_withdraw_amount = balance - total_withdraw_amount
        
        if balance > 0 and request.method == 'POST':
            amount = request.POST.get('amount')
            method = request.POST.get('method')
            bkash_number = request.POST.get('bkash_number')
            paypal_number = request.POST.get('paypal_number')
            nagad_number = request.POST.get('nagad_number')
            user = seller_details

            if len(bkash_number) > 0:
                withdraw = WithDrawModel(
                    amount=amount,
                    user=user,
                    method=method,
                    number=bkash_number,
                    on_review=True,
                    stat="ON REVIEW"
                )
            elif len(paypal_number) > 0:
                withdraw = WithDrawModel(
                    amount=amount,
                    user=user,
                    method=method,
                    number=paypal_number,
                    on_review=True,
                    stat="ON REVIEW"
                )
            else:
                withdraw = WithDrawModel(
                    amount=amount,
                    user=user,
                    method=method,
                    number=nagad_number,
                    on_review=True,
                    stat="ON REVIEW"
                )

            withdraw.save()
            print(withdraw)
            return redirect(f"/earnings/{seller_details.id}")

    # user = seller_details

    args = {
        'seller_details': seller_details,
        'orders_by_seller': orders_by_seller,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "post_seen": post_seen,
        "seller_sees_order": seller_sees_order,
        "cats": cats,
        "total_withdraw_amount": total_withdraw_amount,
        "availabel_withdraw_amount": availabel_withdraw_amount,
    }
        
    return render(request, 'azimpart/earnings.html', args)



def createSellerSendOfferRandomSlug(str_len):
    rand_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k = str_len))
    send_offer = SendOfferModel.objects.filter(send_offer_slug=rand_slug)
    if send_offer.exists():
        createSellerSendOfferRandomSlug(str_len)
    return rand_slug
    
@login_required(login_url='user_login')
@has_selleraccount
def sellerSendOfferView(request, id):
    cats = Category.objects.all().order_by("-id")[:9]
    delivery_time = DeliveryTime.objects.all()
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    try:
        post_request = BuyerPostRequest.objects.get(id=id)
    except BuyerPostRequest.DoesNotExist:
        return redirect("BuyeRequestView")
    else:
        if request.method == "POST":
            send_offer_slug = createSellerSendOfferRandomSlug(20)
            buyer_post_request = post_request
            buyer = post_request.user
            seller = request.user
            description = request.POST.get("description")
            offer_price = request.POST.get("offer_price")
            del_time = request.POST.get("delivery_time")
            
            try:
                del_time = DeliveryTime.objects.get(title=del_time)
            except DeliveryTime.DoesNotExist:
                return redirect(f"/send-offer/{id}/")
            else:
                if description and offer_price:
                    SendOfferModel.objects.create(send_offer_slug=send_offer_slug, buyer_post_request=buyer_post_request,
                                                buyer=buyer, seller=seller, offer_letter=description,
                                                offered_price=offer_price, delivery_time=del_time)
                    buyer_post_request.seller_send_new_offer = False
                    buyer_post_request.save()
                else:
                    messages.error(request, "Please submit all the field!")
                    return redirect(f"/send-offer/{id}/")
                return redirect("BuyeRequestView")

    args = {
        "post_request": post_request,
        "delivery_time": delivery_time,
        "post_seen": post_seen,
        "cats": cats,
        "seller_sees_order": seller_sees_order,
    }
    return render(request, "azimpart/seller_send_offer.html", args)


@login_required(login_url='user_login')
@has_selleraccount
def buyerAllPostsView(request):
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    cats = Category.objects.all().order_by("-id")[:9]
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    buyer_requested_posts = BuyerPostRequest.objects.filter(user=request.user).order_by("-id")
    active_buyer_posts = len(BuyerPostRequest.objects.filter(user=request.user, post_status="ACTIVE"))
    reserved_buyer_posts = len(BuyerPostRequest.objects.filter(user=request.user, post_status="RESERVED"))
    
    send_offers = SendOfferModel.objects.filter(buyer=request.user).order_by("-id")
    requested_offer_posts = 0
    
    for item in send_offers:
        if item.buyer_post_request.post_status != "RESERVED":
            requested_offer_posts += 1
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        for item in not_seen_seller_offers:
            item.seller_send_new_offer = True
            item.save()
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
        
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
    
    args = {
        "offers": offers,
        "buyer_requested_posts": buyer_requested_posts,
        "send_offers": send_offers,
        "cats": cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "order_seen": order_seen,
        "seller_sees_order": seller_sees_order,
        "all_seller_offers_seen": all_seller_offers_seen,
        "active_buyer_posts": active_buyer_posts,
        "reserved_buyer_posts": reserved_buyer_posts,
        "requested_offer_posts": requested_offer_posts,
        
    }
    return render(request, "azimpart/buyer_send_posts.html", args)


@login_required(login_url='user_login')
@has_selleraccount
def deleteBuyerPost(request, id):
    # print(id)
    try:
        requested_post = BuyerPostRequest.objects.get(id=id)
    except BuyerPostRequest.DoesNotExist:
        return redirect("buyer-posts")
    else:
        requested_post.delete()
        return redirect("buyer-posts")


@login_required(login_url='user_login')
@has_selleraccount
def reservedBuyerPost(request, id):
    if request.method == 'POST':
        try:
            buyer_post = BuyerPostRequest.objects.get(id=id)
        except BuyerPostRequest.DoesNotExist:
            return redirect("buyer-posts")
        else:
            buyer_post.post_status = "RESERVED"
            buyer_post.save()
            return redirect("buyer-posts")

@login_required(login_url='user_login')
@has_selleraccount
def activeBuyerPost(request, id):
    if request.method == 'POST':
        try:
            buyer_post = BuyerPostRequest.objects.get(id=id)
        except BuyerPostRequest.DoesNotExist:
            return redirect("buyer-posts")
        else:
            buyer_post.post_status = "ACTIVE"
            buyer_post.save()
            return redirect("buyer-posts")

def refundRequestView(request):
    return render(request, "buyingview/refund-req.html")


############# EXAM ALGO STARTS #################


@login_required(login_url='user_login')
@has_selleraccount
def select_subject_form(request):
    cats = Category.objects.all().order_by("-id")[:9]
    exam_subj = ExamSubject.objects.filter(is_done=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    args = {
        "exam_subj": exam_subj,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "cats": cats,
    }
    return render(request, 'accountview/select_subject.html', args)

# Subject Wise Exam Room


@login_required(login_url='user_login')
@has_selleraccount
def examSuccessView(request):
    return render(request, "azimpart/exam_success.html")


@login_required(login_url='user_login')
@has_selleraccount
def subject_wise_exam_qustion(request, id, *args, **kwargs):
    subject = ExamSubject.objects.all()
    qustion = QustionModel.objects.filter(subject=id)
    cats = Category.objects.all().order_by("-id")[:9]
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    if qustion is not None:
        qus = QustionModel.objects.all().order_by("?")
        qustion = qus.filter(subject=id).last()
        
        if request.method == "POST":
            user = request.user
            attachement = request.FILES.get('attachement')
            
            result = ExamModel(
                user=user,
                attachement=attachement,
                qustion=qustion,
                total_number=0,
                status="PENDING"
            )

            result.save()
            # return HttpResponse("SAVED")
            return redirect("exam-success")
            

    else:
        return HttpResponse("Empty")
    args = {
        "subject": subject,
        "qustion": qustion,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "cats": cats,
    }

    return render(request, "azimpart/exam.html", args)


# def exam_room(request, subject_id):
#     # sub = SellerSubjectChoice.objects.get(pk=subject_id)
#     # subs = SellerSubjectChoice.objects.all()
#     # seller submitted subject wise qustion
#     qustion = QustionModel.objects.random_qustion()

#     if request.method == "POST":
#         user = request.user,
#         attachement = request.FILES.get('attachement')

#         exm = ExamModel(
#             user=user,
#             qustion=qustion,
#             attachement=attachement,
#             status="PENDING"
#         )
#         exm.save()
#         return redirect("/")

#     args = {
#         'qustion': qustion,
#     }
#     return render(request, "azimpart/exam.html", args)




############# EXAM ALGO ENDS #################


# Test #

def read_txt(request):
    pass


# END TEST PART #


# Rafsun Testing Part

def rafsun_header(request):
    return render(request, "rafsunpart/test_header.html")


# azim password reset page
def password_reset_confirm(request):
    return render(request, "accountview/password_reset_confirm.html")
    
    
    
    
# Paypal Success view Here, after successfull payment Checkout paid will update to True


# Paypal Succes URL View Here order will be updated to UNPAID to PAID
def paypal_success(request, id):
    cats = Category.objects.all().order_by("-id")[:9]
    body = json.loads(request.body)
    print("BODY", body)
    order = Checkout.objects.get(pk=id)
    order.paid = True
    order.save()

    args = {
        "order": order,
        "cats": cats,
    }

    return JsonResponse("", safe=False)
    
@login_required(login_url='user_login')
@has_selleraccount    
def payemntTermsView(request):
    user_session = request.session.get("user", None)
    
    cats = Category.objects.all().order_by("-id")[:9]
    
    all_seller_offers_seen = True
    order_seen = True
    
    msg_seen_chatrooms = 0
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, "azimpart/payment_terms.html", args)
    
    

# Review Seller Function
# So it will be (100 * 5 + 70 * 4 + 50 * 3 + 30 * 2 + 20 * 1) / 100 + 70 + 50 + 30 + 20
@login_required(login_url='user_login')
@has_selleraccount
def review_offer(request, checkout_id):
    ratings = Rating.objects.all()
    review = Checkout.objects.get(pk=checkout_id)
    cats = Category.objects.all().order_by("-id")[:9]
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
        
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
        
    if request.method == "POST":
        client = request.user
        seller = review.seller
        text = request.POST.get('text')
        rate = request.POST.get('rate')
        
        if text == None or text == "":
            return redirect(f"/review/{checkout_id}/")
        
        rv = ReviewSeller(
            order=review,
            client=client,
            seller=seller,
            rate_seller=Rating.objects.get(title=rate),
            text=text,
        )
        review.rated = True
        review.save()
        rv.save()
        # Email Function
        
        seller_email = review.seller.email
        email_subject = "YOU GOT AN REVIEW"
        message = render_to_string("mailview/review_seller_email.html", {
            "client": client
        })
        email = EmailMultiAlternatives(email_subject, message, to=[seller_email])
        email.attach_alternative(message, "text/html")
        email.send()
        
        return redirect("review-success")
    
    args = {
        'review': review,
        'ratings': ratings,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "cats": cats,
    }
    return render(request, 'sellingview/review.html', args)
    
    
@login_required(login_url='user_login')
@has_selleraccount   
def reviewSuccessView(request):
    return render(request, "azimpart/review_success.html")

############## PREMIUM OFFER PACKAGE VIEW ####################
@login_required(login_url='user_login')
@has_selleraccount
def premium_offer_package_view(request):
    p_packages = PremiumOfferPackage.objects.all()
    cats = Category.objects.all().order_by("-id")[:9]
    msg_seen_chatrooms = ChatRoom.objects.filter(sellers=request.user, seen=False)
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False

    if len(p_packages) > 0:
        p_pkgs = PremiumOfferPackage.objects.filter(pkg_title="BRONZE")
        p_pkgs2 = PremiumOfferPackage.objects.filter(pkg_title="SILVER")
        p_pkgs3 = PremiumOfferPackage.objects.filter(pkg_title="GOLD")

    args = {
        "p_pkgs": p_pkgs,
        "p_pkgs2": p_pkgs2,
        "p_pkgs3": p_pkgs3,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
        "cats": cats,
    }
    return render(request, "azimpart/premium_package.html", args)

@login_required(login_url='user_login')
@has_selleraccount
def add_package_to_cart(request):
    premium_cart = request.session.get('premium_cart', None)
    pkg_id = request.POST.get('pkg_id')
    
    print(pkg_id)

    # Change #
    if request.method == 'POST':
        if premium_cart is not None:
            print(premium_cart)
            quantity = 1
            # print(quantity)
            if quantity:
                print(len(premium_cart))
                premium_cart.clear()
                if len(premium_cart) >= 1:
                    print("IF PKG ID", pkg_id)
                    premium_cart[pkg_id] = 1
                else:
                    print("ELSE PKG ID", pkg_id)
                    premium_cart[pkg_id] = 1
            # else:
            #     premium_cart[pkg_id] = 1
        else:
            premium_cart = {}
            premium_cart[pkg_id] = 1
        request.session['premium_cart'] = premium_cart

        return redirect("premium_direct_checkout")

@login_required(login_url='user_login')
@has_selleraccount
def premium_direct_checkout(request):
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
        
    cats = Category.objects.all().order_by("-id")[:9]
    premium_cart = request.session.get('premium_cart')
    if not premium_cart:
        request.session['premium_cart'] = {}
    ids = list(request.session.get('premium_cart').keys())
    premium_packages = PremiumOfferPackage.get_package_ids(ids)
    # user = request.user
    off = Offer.objects.filter(user=request.user, offer_status="ACTIVE")
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        address = request.POST.get('addresss')
        user = request.user
        offer_id = request.POST.get('offer_id')
        premium_packages = PremiumOfferPackage.get_package_ids(list(premium_cart.keys()))
        for pp in premium_packages:
            p_checkout = PremiumOfferPackageCheckout(
                first_name=first_name,
                addresss=address,
                user=user,
                pkg=pp,
                offer=Offer.objects.get(id=offer_id),
                quantity=premium_cart.get(str(pp.id)),
                total=pp.price
            )
            p_checkout.save()
            request.session['cart'] = {}
            return redirect("BuyerOrders")

    args = {
        "off": off,
        "premium_packages": premium_packages,
        "cats": cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
    }

    return render(request, "azimpart/package_checkout.html", args)

@login_required(login_url='user_login')
@has_selleraccount
def premium_payment(request, id, *args, **kwargs):
    cats = Category.objects.all().order_by("-id")[:9]
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
        
    premium_details = PremiumOfferPackageCheckout.objects.get(pk=id)
    if request.method == 'POST':
        settings = {
                'store_id': 'testbox', 'store_pass': 'qwerty', 'issandbox': True
            }
        premium_details = PremiumOfferPackageCheckout.objects.get(pk=id)
        user = request.user
        first_name = premium_details.first_name
        address = premium_details.addresss
        email = premium_details.user.email
        phone_number = request.user.selleraccount.contact_no
        country = request.user.selleraccount.country
        city = request.user.selleraccount.city
        # package_category = premium_details.package.offer.category
        quantity = premium_details.quantity
        total = premium_details.total * 86
        transaction_id = premium_details.id

        # Checkout.objects.filter(pk=kwargs['id'])
        PremiumOfferPackageCheckout.objects.get(pk=id)

        sslcommerz1 = SSLCOMMERZ(settings)
        post_body1 = {}
        post_body1['total_amount'] = total
        post_body1['currency'] = "BDT"
        # post_bo1dy1['tran_id'] = "STFU"
        post_body1['tran_id'] = transaction_id
        post_body1['success_url'] = "https://marketage.io/premium-success/"
        post_body1['fail_url'] = "https://marketage.io/premium-failed/"
        post_body1['cancel_url'] = "https://marketage.io/premium-cancel/"
        post_body1['emi_option'] = 0
        post_body1['cus_name'] = first_name
        post_body1['cus_email'] = email
        post_body1['cus_add1'] = "N/A"
        post_body1['cus_phone'] = phone_number
        post_body1['cus_city'] = city
        post_body1['cus_country'] = country
        post_body1['shipping_method'] = "NO"
        post_body1['multi_card_name'] = ""
        post_body1['num_of_item'] = "1"
        post_body1['product_name'] = premium_details.pkg
        post_body1['product_category'] = "DIGITAL"
        post_body1['product_profile'] = "general"
        print(post_body1)
        response = sslcommerz1.createSession(post_body1)
        print(response)
        return redirect(response['GatewayPageURL'])
        # return redirect(response['failedreason'])
        # return HttpResponse("HAHA")
    args = {
        "premium_details": premium_details,
        "cats": cats,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
    }
    return render(request, "azimpart/premium_payment.html", args)

@login_required(login_url='user_login')
@has_selleraccount
@csrf_exempt
def premium_successView(request):
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
    
    if request.POST.get('status') == "VALID":
        tran_id = request.POST['tran_id']
        # print("TRAIN ID:", tran_id)
        try:
            premium_details = PremiumOfferPackageCheckout.objects.get(id=tran_id)
        except:
            return redirect("BuyerOrders")
        else:
            premium_details.is_paid = True
            premium_details.status = "ACTIVE"
            premium_details.offer.is_premium=True
            premium_details.offer.save()
            premium_details.save()
            print(premium_details.pkg.pkg_title)

            offer_detail = premium_details.offer

            if premium_details.pkg.pkg_title == "BRONZE":
                offer_detail.is_bronze = True
                offer_detail.is_silver = False
                offer_detail.is_gold = False
                offer_detail.bronze_created = datetime.now()
                offer_detail.silver_created = None
                offer_detail.gold_created = None
            elif premium_details.pkg.pkg_title == "SILVER":
                offer_detail.is_silver = True
                offer_detail.is_bronze = False
                offer_detail.is_gold = False
                offer_detail.silver_created = datetime.now()
                offer_detail.bronze_created = None
                offer_detail.gold_created = None
            elif premium_details.pkg.pkg_title == "GOLD":
                offer_detail.is_gold = True
                offer_detail.is_silver = False
                offer_detail.is_bronze = False
                offer_detail.gold_created = datetime.now()
                offer_detail.bronze_created = None
                offer_detail.silver_created = None

            offer_detail.save()
            # Sending Email To USER
            rec = premium_details.user.email
            dura = premium_details.pkg.duration
            email_subejct = "PAYMENT SUCCESSFULL FOR YOUR PREMIUM OFFER"
            email_message = render_to_string("mailview/premium_offer_success_mail.html", {
                "dura": dura
            })
            email = EmailMultiAlternatives(email_subejct, email_message, to=[rec])
            email.attach_alternative(email_message, "text/html")
            email.send()
            
    args = {
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
    }

        
    return render(request, "responseview/premium_success.html", args)


@login_required(login_url='user_login')
@has_selleraccount
@csrf_exempt
def premiumfailedView(request):
    return render(request, "responseview/premium_failed.html")


@login_required(login_url='user_login')
@has_selleraccount
@csrf_exempt
def premiumcancelledView(request):
    return render(request, "responseview/premium_cancel.html")
    
    
# 404 page view
def page_404View(request):
    return render(request, "error/404.html")



# Child Category Wise Offers
@login_required(login_url='user_login')
def get_child_category_wise_offers(request, id, slug, *args, **kwargs):
    try:
        single_childcat = ChildSubcategory.objects.get(child_slug=slug, id=id)
    except ChildSubcategory.DoesNotExist:
        return redirect("buying_view")
        
    cats = Category.objects.all().order_by("-id")[:9]
    child_wise_offers = Offer.objects.filter(child_subcategory__child_slug=slug, offer_status="ACTIVE")
    
    subcategory = Subcategory.objects.all()
    user_session = request.session.get("user", None)
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    
    msg_seen_chatrooms = 0
    all_seller_offers_seen = True
    order_seen = True
    
    if user_session is not None:
        msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
        # Seller all offers seen notify
        not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
        
        if len(not_seen_seller_offers) > 0:
            all_seller_offers_seen = False
        
        # Buyer order notify
        orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
        
        
        if len(orders) > 0:
            order_seen = False
            
    args = {
        "single_childcat": single_childcat,
        "child_wise_offers": child_wise_offers,
        "all_seller_offers_seen": all_seller_offers_seen,
        "order_seen": order_seen,
        "subcategory": subcategory,
        "cats": cats,
        "offers": offers,
        "msg_seen_chatrooms": msg_seen_chatrooms,
    }
    return render(request, "buyingview/child_wise_offers.html", args)
    
    
# manual paymeny Function


def pay_manually(request, id, *args, **kwargs):
    order_id = Checkout.objects.get(pk=id)
    total_total = order_id.grand_total * 86
    khoroch = total_total * 2/100
    khoroch_total = total_total + khoroch
    
    total_bdt = order_id.grand_total * 86
    if request.method =="POST":
        trx_number = request.POST.get('trx_number')
        phone_number = request.POST.get('phone_number')
        method = request.POST.get("method")
        manualpayment = ManualPayment(
            trx_number=trx_number,
            phone_number=phone_number,
            method=method,
            orderId=order_id,
            rec=khoroch_total
            
        )
        
        manualpayment.save()
        order_id.order_status = "ACTIVE"
        order_id.save()
        buyer = request.user.email
        mail_subject = "You Order has been Placed"
        mail_message = render_to_string('mailview/order-complete.html', {
            
        })
        email = EmailMultiAlternatives(mail_subject, mail_message, to=[buyer])
        email.attach_alternative(mail_message, "text/html")
        email.send()
        
        # Sending Mail to seller
        orderId = order_id.id
        seller = order_id.seller.email
        mail_subject2 = "You got a new order!"
        mail_message2 = render_to_string("mailview/seller_confirmation.html", {
            "buyer": buyer,
            "orderId": orderId
        })
        email2 = EmailMultiAlternatives(mail_subject2, mail_message2, to=[seller])
        email2.attach_alternative(mail_message2, "text/html")
        email2.send()
        
        
        

        return redirect("success")
    args = {
        "khoroch_total": khoroch_total,
        "total_total": total_total,
        "khoroch": khoroch,
        "total_bdt": total_bdt
    }
    return render(request, "azimpart/manual_payment.html", args)
    
    
    
    # email_subject = "Order Has been Placed Please Pay Now"
    #         email_message = render_to_string('mailview/order-complete.html', {
                
    #         })
            
    #         email = EmailMultiAlternatives(email_subject, email_message, to=[rec])
    #         email.attach_alternative(email_message, "text/html")
    
    



# Campaigns Function
@login_required(login_url='user_login')
@has_selleraccount
def campaignPageView(request):
    campaigns = CampaignModel.objects.all()
    seller_set = set()
    seller_campaigns = SubmissionForCampaign.objects.filter(user=request.user, attend_exam=True)
    
    for item in seller_campaigns:
        seller_set.add(item.campaign)
    
    msg_seen_chatrooms = ChatRoom.objects.filter(buyer=request.user, seen=False)
    cats = Category.objects.all().order_by("-id")[:9]
    # Seller all offers seen notify
    not_seen_seller_offers = BuyerPostRequest.objects.filter(user=request.user, seller_send_new_offer=False)
    all_seller_offers_seen = True
    
    offers = Offer.objects.filter(offer_status="ACTIVE").order_by('-click')
    
    # Seller's order notification
    seller_sees_order = True
    not_seen_orders = Checkout.objects.filter(seller=request.user, order_is_seen=False, paid=True)
    
    if len(not_seen_orders) > 0:
        seller_sees_order = False
    
    # Buyer post notify
    all_buyer_posts = BuyerPostRequest.objects.all()
    all_buyer_posts_seen_user = BuyerPostRequest.objects.filter(seen_users=request.user)
    
    post_seen = True
    
    if len(all_buyer_posts_seen_user) != len(all_buyer_posts):
        post_seen = False
    
    if len(not_seen_seller_offers) > 0:
        all_seller_offers_seen = False
    
    # Buyer order notify
    orders = Checkout.objects.filter(user=request.user, order_submitted_is_seen=False)
    
    order_seen = True
    
    if len(orders) > 0:
        order_seen = False
        
    campaign_banners = CampaignBanner.objects.all()
    
    args = {
        "order_seen": order_seen,
        "all_seller_offers_seen": all_seller_offers_seen,
        "msg_seen_chatrooms": msg_seen_chatrooms,
        "cats": cats,
        "seller_sees_order": seller_sees_order,
        "post_seen": post_seen,
        "offers": offers,
        "campaigns": campaigns,
        "seller_set": seller_set,
        "campaign_banners": campaign_banners,
    }
    return render(request, "campaign_folder/campaigns.html", args)



# Campaign wise Qustion Function or view
@login_required(login_url='user_login')
@has_selleraccount
def get_campaigns_qustion_submit_answer(request, id, *args, **kwargs):
    try:
        campaign = CampaignModel.objects.get(pk=id)
    except:
        return render("get_campaign_page")
    else:
        camp_quest = QustionsForCampaign.objects.get(title_of_qustion=campaign.qustion_for_campaign)
        
        if request.method == "POST":
            user = request.user
            campaign = campaign
            uploads = request.FILES.get("uploads")
            rate = "NOT RATED YET"
            status = "ON REVIEW"
            attend_exam = True
    
            sv = SubmissionForCampaign(
                user=user,
                campaign=campaign,
                uploads=uploads,
                rate=rate,
                status=status,
                attend_exam=attend_exam
            )
    
            try:
                sv.save()
                return redirect("success-response")
            except:
                return HttpResponse("Something went Wrong")


    args = {
        "camp_quest": camp_quest,
    }
    return render(request, "campaign_folder/qustion_and_submit.html", args)


# Success Response View
@login_required(login_url='user_login')
@has_selleraccount
def get_success_response(request, *args, **kwargs):
    args ={}
    return render(request, "campaign_folder/success_response.html", args)
    
    
    


