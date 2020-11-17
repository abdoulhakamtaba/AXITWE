from django.db import models
from django.shortcuts import reverse
from django.conf import settings


# Create your models here.

'''
User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username
'''
####### LES CATEGORIES #############
class Category(models.Model):
    name_category = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField()
    top_category = models.BooleanField(default=False)

    def __str__(self):
        return self.name_category

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_subcategory = models.CharField(blank=True, null=True, max_length=100)


    def __str__(self):
        return self.name_subcategory

####### LES VILLES #############
class Ville(models.Model):
    name_ville = models.CharField(blank=True, null=True, max_length=100)
    image = models.ImageField()

    def __str__(self):
        return self.name_ville

class Quartier(models.Model):
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    name_quartier = models.CharField(blank=True, null=True, max_length=100)


    def __str__(self):
        return self.name_quartier

class Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    call_number = models.CharField(max_length=8)
    whatsapp_number = models.CharField(max_length=8)
    location = models.CharField(max_length=100)
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(blank=True, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=False)
    negotiable = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={
            'slug':self.slug
        })
    
    def get_update_product(self):
        return reverse('update-product', kwargs={
            'slug': self.slug
        })
    def get_delete_product(self):
        return reverse('delete-product', kwargs={
            'slug': self.slug
        })

    def get_images_product(self):
        return reverse('photo-product', kwargs={
            'slug': self.slug
        })

class PostImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/images')

    def __str__(self):
        return self.item.title


class UserName(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_user')
    username = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
