from django.contrib import admin
from .models import Item, PostImage, Category, Subcategory, Ville, Quartier, UserName #ItemVariation,

# Register your models here.



'''
class ItemVariationAdmin(admin.ModelAdmin):
    list_display = [
        'item',
        'value',
    ]

    list_filter=[
        'item',
    ]

    search_fields = ['value']
'''


######## LES PHOTOS ###############
class PhotoVariationInLineAdmin(admin.TabularInline):
    model = PostImage
    extra = 1

class PhotoAdmin(admin.ModelAdmin):
    inlines = [PhotoVariationInLineAdmin]

###### LES CATEGORY ################
class CategoryVariationInLineAdmin(admin.TabularInline):
    model = Subcategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryVariationInLineAdmin]

######### LES VILLES #################
class VilleVariationInLineAdmin(admin.TabularInline):
    model = Quartier
    extra = 1

class VilleAdmin(admin.ModelAdmin):
    inlines = [VilleVariationInLineAdmin]

#admin.site.register(ItemVariation, ItemVariationAdmin)
admin.site.register(Item, PhotoAdmin)
#admin.site.register(OrderItem)
#admin.site.register(likeItem)
#admin.site.register(Order)
admin.site.register(PostImage)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Ville, VilleAdmin)
admin.site.register(Quartier)
admin.site.register(UserName)