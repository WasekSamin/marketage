from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class OfferManagerInline(admin.TabularInline):
    model = OfferManager

class OfferAdmin(admin.ModelAdmin):
    inlines = [
        OfferManagerInline
    ]
    list_display = ["id", "offer_title", "category", "sub_category"]
    search_fields = ["category__title", "sub_category__sub_title"]

admin.site.register(OfferManager)
admin.site.register(Country)
admin.site.register(Package)
admin.site.register(SellerAccount)
admin.site.register(Services)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Tag)
admin.site.register(DeliveryTime)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Currency)
admin.site.register(DummyUser)
admin.site.register(LandingSlider)
admin.site.register(SecondarySlider)
@admin.register(SellerSubmit)
class SellerSubmitAdmin(admin.ModelAdmin):
    list_display = ("id", "checkout")
admin.site.register(PromoCode)
admin.site.register(BuyerPostRequest)
admin.site.register(CategoryInterestedModel)
admin.site.register(ExtraImage)
admin.site.register(Revision)
admin.site.register(NumberOfPage)
admin.site.register(SendOfferModel)

admin.site.register(WithDrawModel)
admin.site.register(ChildSubcategory)
admin.site.register(SupportCategoryModel)
admin.site.register(SupportModel)
admin.site.register(Rating)
admin.site.register(ReviewSeller)
admin.site.register(PremiumOfferPackage)
admin.site.register(PremiumOfferPackageCheckout)
admin.site.register(ExamSubject)
admin.site.register(QustionModel)
admin.site.register(ExamModel)
admin.site.register(NotificationModel)
admin.site.register(ManualPayment)
admin.site.register(QustionsForCampaign)
admin.site.register(CampaignModel)
admin.site.register(SubmissionForCampaign)
admin.site.register(CampaignBanner)


@admin.register(Checkout)
class ChekckoutAdmin(admin.ModelAdmin):
    list_display = ("id", "slug")
    