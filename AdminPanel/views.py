from django.core.mail import send_mail
from django.core.mail.message import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from AdminPanel.models import SendEmailToUser
from mainApp.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

def adminLoginView(request):
    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser == True:
            login(request, user)
            return redirect("AdminHome")
        else:
            messages.error(request, "You are not the manager.")
            return redirect("admin-login")
        
    return render(request, "admin_login.html")



def adminlogoutview(request):
    logout(request)
    return redirect('admin-login')



@login_required(login_url="admin-login")
def get_adminpanel_url(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    orders = Checkout.objects.all().order_by('-id')
    count_order = Checkout.objects.all().count()
    count_offers = Offer.objects.all().count()

    completed_orders = Checkout.objects.filter(is_complete=True, paid=True).count()

    increase = completed_orders / 100

    orders_paginator = Paginator(orders, 10)

    page_number = request.GET.get('page')

    orders_obj = orders_paginator.get_page(page_number)
    # Notifcation Object
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting The order is checked or not For Checkout Model
    count_unseen_order = Checkout.objects.filter(is_checked=False).count()
    # Count All Active Users
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
    # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)

    # Checking and counting new Transactions
    new_tran = Checkout.objects.filter(paid=True).count()

    # Checking All Notifications
    notifications = NotificationModel.objects.all().order_by("-id")[:6]

    args = {
        "orders": orders,
        "orders_obj": orders_obj,
        "count_order": count_order,
        "count_offers": count_offers,
        "increase": increase,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_unseen_order": count_unseen_order,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers,
        "notifications": notifications
    }
    return render(request, 'admin_panel.html', args)



@login_required(login_url="admin-login")
def order_details(request, id):
    order_details = Checkout.objects.get(pk=id)
    order_details.is_checked = True
    order_details.save()
    nots = NotificationModel.objects.filter(has_checked=False).count()
    args = {
        "order_details": order_details,
        "nots": nots,
    }

    return render(request, "admin_order_Details.html", args)



@login_required(login_url="admin-login")
def uploadedOfferView(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    all_offers = Offer.objects.all().order_by('-id')
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting The order is checked or not For Checkout Model
    count_unseen_order = Checkout.objects.filter(is_checked=False).count()
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
    # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)
    args = {    
        "all_offers": all_offers,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_unseen_order": count_unseen_order,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers
    }
    return render(request, "uploaded_offer.html", args)



# Edit Offer for admin panel
@login_required(login_url="admin-login")
def admin_edit_offer(request, id, slug):
    offer_details = Offer.objects.get(pk=id, slug=slug)
    offer_details.has_checked = True
    offer_details.save()
    basic_package, standard_package, premium_package = None, None, None
    basic_deliveries, standard_deliveries, premium_deliveries = None, None, None
    basic_num_pages, standard_num_pages, premium_num_pages = None, None, None
    basic_revisions, standard_revisions, premium_revisions = None, None, None
    basic_price, standard_price, premium_price = None, None, None
    document = None, 
    offer_first_img, offer_second_img, offer_third_img = None, None, None

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
            admin_post_status = request.POST.get("admin_post_status")
            
            if admin_post_status:
                offer.offer_status = admin_post_status
                if admin_post_status == "ACTIVE":
                    offer.is_pending = False
                
                offer.save()
                
                return redirect("uploaded-offer")
            

    args = {
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
    }
    return render(request, 'admin_edit_offer.html', args)



@login_required(login_url="admin-login")
def allUsersView(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    users = User.objects.exclude(username=request.user).order_by('-id')
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting all Active users
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
       # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)
    args = {
        "users": users,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers,
    }

    return render(request, "all_users.html", args)


@login_required(login_url="admin-login")
def allOrdersView(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    orders = Checkout.objects.all().order_by('-id')
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting The order is checked or not For Checkout Model
    count_unseen_order = Checkout.objects.filter(is_checked=False).count()
    # Counting all Active users
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
       # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)
    args = {
        "orders": orders,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_unseen_order": count_unseen_order,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers,
    }
    return render(request, "all_order.html", args)



@login_required(login_url="admin-login")
def transactionView(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    transactions = Checkout.objects.filter(paid=True)
    completed_orders = Checkout.objects.filter(is_complete=True).count()
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting The order is checked or not For Checkout Model
    count_unseen_order = Checkout.objects.filter(is_checked=False).count()
    # Counting all Active users
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
       # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)
    completed_orders = Checkout.objects.filter(is_complete=True, paid=True).count()
    increase = (completed_orders / 100)
    args = {
        'transactions': transactions,
        'increase': increase,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_unseen_order": count_unseen_order,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers,
        "completed_orders": completed_orders
    }
    return render(request, "transactions.html", args)



@login_required(login_url="admin-login")
def withdrawView(request):
    user = request.user
    if user.is_superuser == False:
        return redirect("buying_view")
    withdraws = WithDrawModel.objects.filter(on_review=True).order_by('-id')
    nots = NotificationModel.objects.filter(has_checked=False).count()
    # Counting checked or not checked for ExamModel
    count_check_exm = ExamModel.objects.filter(has_checked=False).count()
    # Counting The order is checked or not For Checkout Model
    count_unseen_order = Checkout.objects.filter(is_checked=False).count()
    # Counting all Active users
    count_users = User.objects.all().count()
    # If there is a new withdraw request it will show a pointer
    new_with = WithDrawModel.objects.filter(is_new=False)
       # Counting Recent Upload Offers
    recent_offers = Offer.objects.filter(has_checked=False)
    args = {
        'withdraws': withdraws,
        "nots": nots,
        "count_check_exm": count_check_exm,
        "count_unseen_order": count_unseen_order,
        "count_users": count_users,
        "new_with": new_with,
        "recent_offers": recent_offers,
    }
    return render(request, "withdraw.html", args)


@login_required(login_url="admin-login")
def clear_amount(request, id):
    clear_wd = WithDrawModel.objects.get(pk=id)
    clear_wd.is_new = True
    clear_wd.save()
    order_by_seller = Checkout.objects.filter(seller =clear_wd.user)
    if request.method == "POST":
        method = request.POST.get('method')
        amount = clear_wd.amount
        user = clear_wd.user
        stat = request.POST.get('stat')

        clear_wd.stat = stat
        clear_wd.is_new = True
        clear_wd.save()
        
        clear_wd.user.selleraccount.withdrawn += amount
        clear_wd.user.selleraccount.wallet -= clear_wd.amount
        print("HEREEE" + str(clear_wd.amount))
        clear_wd.user.selleraccount.save()
        # Sending email to Seller
        withdraw_amount = clear_wd.user.selleraccount.withdrawn

        if clear_wd.stat == "CLEARED":
            mail_subject = "CONGRATS! YOU HAVE RECEIVED YOUR REQUESTED MONEY"
            message = render_to_string("adminmailview/clear-amount-email.html", {
                    'user': user,
                    'withdraw_amount': withdraw_amount,
                })
            send_mail = str(clear_wd.user.email)
            email_email = EmailMultiAlternatives(mail_subject, message, to=[send_mail])
            
            email_email.attach_alternative(message, "text/html")
            try:
                email_email.send()
            except:
                return HttpResponse("ERROR 404!")
            print(str(email_email))
            email_email.send()
        elif clear_wd.stat == "REJECTED":
            mail_subject = "YOUR REUQESTED WITHDRAW HAS BEEN REJECTED!"
            message = render_to_string("adminmailview/clear-amount-email.html", {
                    'user': user,
                    'withdraw_amount': withdraw_amount,
                })
            send_mail = str(clear_wd.user.email)
            email_email = EmailMultiAlternatives(mail_subject, message, to=[send_mail])
            
            email_email.attach_alternative(message, "text/html")
            try:
                email_email.send()
            except:
                return HttpResponse("ERROR 404!")
            print(str(email_email))
            email_email.send()

        # return HttpResponse("SUCCESS")
        return redirect("WithdrawView")
    args = {
        "clear_wd": clear_wd,
        "order_by_seller": order_by_seller,
    }

    return render(request, "withdraw_details.html", args)



@login_required(login_url="admin-login")
def get_exam_room_page(request, *args, **kwargs):
    try:
        user = request.user
        if user.is_superuser == False:
            return redirect("buying_view")
        exam_models = ExamModel.objects.all().order_by('-id')
        nots = NotificationModel.objects.filter(has_checked=False).count()
        # Counting checked or not checked for ExamModel
        count_check_exm = ExamModel.objects.filter(has_checked=False).count()
        # Counting The order is checked or not For Checkout Model
        count_unseen_order = Checkout.objects.filter(is_checked=False).count()
        # Counting all Active users
        count_users = User.objects.all().count()
        # If there is a new withdraw request it will show a pointer
        new_with = WithDrawModel.objects.filter(is_new=False)
           # Counting Recent Upload Offers
        recent_offers = Offer.objects.filter(has_checked=False)
        args = {
            "exam_models": exam_models,
            "nots": nots,
            "count_check_exm": count_check_exm,
            "count_unseen_order": count_unseen_order,
            "count_users": count_users,
            "new_with": new_with,
            "recent_offers": recent_offers,
        }
        return render(request, "exam_model.html", args)
    except:
        return HttpResponse("404 NOT FOUND")



@login_required(login_url="admin-login")
def get_exam_room_details_url(request, id, *args, **kwargs):
    try:
        user = request.user
        if user.is_superuser == False:
            return redirect("buying_view")
        exam_details =ExamModel.objects.get(pk=id)
        nots = NotificationModel.objects.filter(has_checked=False).count()

        exam_details.has_checked = True
        exam_details.save()

        if request.method == "POST":
            # updating marks and status for exam model
            total_number = request.POST.get('total_number')
            status = request.POST.get('status')

            exam_details.update(
                total_number=total_number,
                status=status
            )
            return HttpResponse("SUCCESS")
        args = {
            "exam_details": exam_details,
            "nots": nots
        }
        return render(request, "exam_details.html", args)
    except:
        return HttpResponse("404 NOT FOUND")


@login_required(login_url="admin-login")
def get_notification(request, *args, **kwargs):
    try:
        user = request.user
        if user.is_superuser == False:
            return redirect("buying_view")
        notifications = NotificationModel.objects.all().order_by('-id')
        
        nots = NotificationModel.objects.filter(has_checked=False).count()
        # Counting checked or not checked for ExamModel
        count_check_exm = ExamModel.objects.filter(has_checked=False).count()
        # Counting The order is checked or not For Checkout Model
        count_unseen_order = Checkout.objects.filter(is_checked=False).count()
        # Counting all Active users
        count_users = User.objects.all().count()
        # If there is a new withdraw request it will show a pointer
        new_with = WithDrawModel.objects.filter(is_new=False)
           # Counting Recent Upload Offers
        recent_offers = Offer.objects.filter(has_checked=False)
        args = {
            "notifications": notifications,
            "nots": nots,
            "count_check_exm": count_check_exm,
            "count_unseen_order": count_unseen_order,
            "count_users": count_users,
            "new_with": new_with,
            "recent_offers": recent_offers,
        }
        return render(request, "notifications.html", args)
    except OverflowError:
        return HttpResponse("PAGE NOT WORKING TRY AGAIN!")



@login_required(login_url="admin-login")
def get_notificatiion_details_url(request, id, *args, **kwargs):
    try:
        user = request.user
        if user.is_superuser == False:
            return redirect("buying_view")
        notification_details = NotificationModel.objects.filter(pk=id).last()
        notification_details.has_checked = True
        notification_details.save()

        nots = NotificationModel.objects.filter(has_checked=False).count()

        args = {
            "notification_details": notification_details,
            "nots": nots
        }
        return render(request, 'notification_details.html', args)
    except OverflowError as e:
        return e


def get_manual_transaction_page(request):
    mans = ManualPayment.objects.all()
    
    args = {
        "mans": mans,
        
    }
    return render(request, "manual_transaction.html", args)

# update manual payment status

def update_manual_payment(request, id):
    payment_details = ManualPayment.objects.get(pk=id)
    
    if request.method=="POST":
        status = request.POST.get("status")
        
        payment_details.status = status
        
        payment_details.save()
        
        if payment_details.status == "DONE":
            payment_details.orderId.paid = True
            payment_details.orderId.save()
            payment_details.orderId.order_status = "ACTIVE"
            payment_details.orderId.save()
        
        nv = NotificationModel(
            orderId=payment_details.orderId,
            user=payment_details.orderId.user,
            title="1 New Notification",
            content="NEW MANUAL TRANSACTION PLEASE CHECK THE DETAILS",
            
            )
        nv.save()
        # Email Sending TO manager
        
        rec = request.user.email
        email_subject = "1 new notification"
        email_message = render_to_string("adminmailview/manual_payment_email.html", {
            
        })
        email = EmailMultiAlternatives(email_subject, email_message, to=["notification@marketage.io"])
        email.attach_alternative(email_message, "text/html")
        
        email.send()
        
        # Email sending to Buyer
        
        buyer = payment_details.orderId.user.email
        subj = "THANK YOU FOR PLACING AN ORDER"
        msg = render_to_string("adminmailview/buyer_success_email.html", {})
        
        mail = EmailMultiAlternatives(subj, msg, to=[buyer])
        mail.attach_alternative(msg, "text/html")
        mail.send()
        
        return redirect("get_manual_transaction_page")
    
    
    args = {
        "payment_details": payment_details
    }
    return render(request, "payment_details.html", args)




def send_email_to_user(request, *args, **kwargs):
    users = User.objects.exclude(username=request.user)
    if request.method == "POST":
        sender = request.user
        receiver = request.POST.get('receiver')
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        send = SendEmailToUser(
            sender = sender,
            receiver = receiver,
            subject=subject,
            content = content,
        )
        send.save()
        
        test = "itna.sakib@gmail.com"
        send_mail(
            subject,
            content,
            # 'itna.sakib@gmail.com',
            'noreply@marketage.io',
            [receiver],
            fail_silently=False
        )
        return HttpResponse("Success")
    args = {
        "users": users
        }
    return render(request, "adminmailview/send_mail_to_user.html", args)