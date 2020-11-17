from django.urls import path
from .views import homePage, productsPage, product_detail, contactPage, search, sellProduct, updateProduct, updateProductOnly, deleteProduct, imagesUpload, chooseCategory,productsPageDetail, productsPageSubDetail, chooseSubcategory, villes, tous_category, tous_villes, chooseCategoryUpdate, chooseSubcategoryUpdate, changeUserName

urlpatterns = [
    path('', homePage, name='shop-home'),
    path('contact/', contactPage, name='shop-contact'),
    path('products/', productsPage, name='products-page'),
    path('products-detail/<arg>/<args>/', productsPageDetail, name='products-page-detail'),
    path('products-subcat-detail/<argu>/<args>/', productsPageSubDetail, name='products-page-subcat-detail'),
    path('products/<slug>/', product_detail, name='product-detail'),

    path('search-results/', search, name='search'),

    path('sell/<args>/', sellProduct, name='sell'),
    path('update-product/<slug>/', updateProductOnly, name='update-product-only'),
    path('update-product/<slug>/<args>/', updateProduct, name='update-product'),
    path('delete-product/<slug>/', deleteProduct, name='delete-product'),

    path('photos-products/<slug>/', imagesUpload, name='photo-product'),

    path('categories/', chooseCategory, name='category'),
    path('categories/<argum>/', chooseSubcategory, name='sub-category'),
    path('categories-update/<slug>/', chooseCategoryUpdate, name='category-update'),
    path('sub-categories-update/<argum>/<slug>/', chooseSubcategoryUpdate, name='sub-category-update'),
    

    path('villes/<arg>/<args>/', villes, name='ville'),
    
    path('tous-category/<args>/', tous_category, name='tous-category'),
    path('tous-villes/<args>/', tous_villes, name='tous-villes'),

    path('change-username/', changeUserName, name='user_name'),
    
]