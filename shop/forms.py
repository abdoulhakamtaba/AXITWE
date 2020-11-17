from django import forms
from .models import Item, PostImage, UserName #ItemVariation
#from django_countries.fields import CountryField
#from django_countries.widgets import CountrySelectWidget


class SellPostForm(forms.ModelForm):

    title = forms.CharField(label='Nom du produit',widget=forms.TextInput(attrs={
        'placeholder':"Enter your Item. Ex: T-shirt",
        'class':'form-marg',
    }))

    location = forms.CharField(label='Ville et Quartier',widget=forms.TextInput(attrs={
        'placeholder':"Ex: Calavi, kpota.",
        'class':'form-marg',
    }))

    description = forms.CharField(label='Description du produit' ,widget=forms.Textarea(attrs={
        'placeholder':"Decrire le produit en detail pour convaincre l'acheteur.",
        'class':'form-marg',
    }))
    
    image = forms.ImageField(label='IMAGE (select only one image)')
    price = forms.CharField(label='Prix du produit', widget=forms.NumberInput())
    negotiable = forms.BooleanField(label='Prix Negotiable (Si oui cocher la case.)', required=False)
    new = forms.BooleanField(label='Est-ce nouceau? (Si oui cocher la case.)', required=False)

    call_number = forms.CharField(label='Numero de telephone',widget=forms.TextInput(attrs={
        'placeholder':"Mettez votre numro sans '+229' ",
    }))

    whatsapp_number = forms.CharField(label='Numero Whatsapp',widget=forms.TextInput(attrs={
        'placeholder':"Mettez votre numro sans '+229' ",
        'class':'form-marg',
    }))

    class Meta:
        model = Item
        fields=('location', 'title', 'price','negotiable', 'description', 'image', 'new', 'call_number', 'whatsapp_number')



class PhotoForm(forms.ModelForm):

    class Meta:
        model = PostImage
        fields=()


class UserNamePostForm(forms.ModelForm):

    

    class Meta:
        model = UserName
        fields=('username',)

