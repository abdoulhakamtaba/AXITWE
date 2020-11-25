from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from .models import Item, PostImage, Category, Subcategory, Ville, Quartier, UserName
from my_account.models import MyAccount
from .forms import SellPostForm, PhotoForm, UserNamePostForm
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
import phonenumbers, os, random, string
from PIL import Image
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


####### ITEM ORDER BY ############
def order_by_cash(item, request):

    try:

        select_sort = request.GET.get('select_sort')
        if select_sort == 'Price: $$ - $':
            return item.order_by('-price')

        elif select_sort == 'Price: $ - $$':
            return item.order_by('price')
        elif select_sort == 'newest':
            return item.order_by('-timestamp')
        else:
            return item
    
    except:
        return item

########## PAGINATOR ###########
def paginatora(request, itemo):
    res_per_page = 6
    paginator = Paginator(itemo, res_per_page)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset= paginator.page(paginator.num_pages)

    result = []
    result.append(paginated_queryset)
    result.append(page_request_var)
    result.append(res_per_page)

    return result

######### SEARCH FOR ITEM #####
def search(request):
    queryset = Item.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
        ).distinct()

    catos = {}
    villos = {}
    vi_len = 0

    categorie = Category.objects.all()
    villes = Ville.objects.all()
    for vi in villes:
        it = Item.objects.filter(location__icontains = vi)
        villos[vi]=len(it)
        vi_len = vi_len+len(it)


    for every_cat in categorie:
        subcategory=Subcategory.objects.filter(category=every_cat)
        cat_len = 0
        for every_sub_cat in subcategory:
            item = Item.objects.filter(category=every_sub_cat)
            cat_len = cat_len+len(item)

        catos[every_cat] = cat_len

    itemss = order_by_cash(queryset, request)

    res = paginatora(request, itemss)

    found = len(queryset)
    if found<=res[2]:
        result_per_p = found
    else:
        result_per_p= res[2]

    select_cat = 'Category'
    select_city = 'Villes'

    querysetos = {}

    for every_it in res[0]:
        imo = PostImage.objects.filter(item=every_it)
        querysetos[every_it]=imo

    context = {
        'queryset':querysetos,
        'category':categorie,
        'found':found,
        'page_request_var':res[1],
        'villos':villos,
        'catos':catos,
        'result_per_p':result_per_p,
        'select_cat':select_cat,
        'select_city':select_city,
        'vi_len':vi_len,
    }
    return render(request, 'results.html', context)



########## SHOP #########
def homePage(request):
    items = Item.objects.all()
    #count_order_item = 0
    #if request.user.is_authenticated:
    #    count_order_item = OrderItem.objects.filter(user = request.user).count()
    #else:
    #    count_order_item = 0

    categories=Category.objects.all()
    top_cat = Category.objects.filter(top_category=True)
    ville = Ville.objects.all()


    context = {
        'item':items,
        'categories':categories,
        'villos':ville,
        'top_cat':top_cat,
    }

    return render (request, 'index.html', context)

######## CONTACT ##########
def contactPage(request):

    return render (request, 'contact.html')



########## PRODUCTS ###########
def productsPage(request):
    items = Item.objects.all()
    it_len = 0
    vi_len = 0
    catos = {}
    villos = {}

    categorie = Category.objects.all()
    villes = Ville.objects.all()
    for vi in villes:
        it = Item.objects.filter(location__icontains = vi)
        villos[vi]=len(it)
        vi_len = vi_len+len(it)

    for every_cat in categorie:
        subcategory=Subcategory.objects.filter(category=every_cat)
        cat_len = 0
        for every_sub_cat in subcategory:
            item = Item.objects.filter(category=every_sub_cat)
            cat_len = cat_len+len(item)
            it_len = it_len+len(item)

        catos[every_cat] = cat_len
        

    cato=True
    cato1 = False
    cato2 = False

    itemss = order_by_cash(items, request)

    res = paginatora(request, itemss)
    if it_len< res[2]:
        result_per_p = it_len
    else:
        result_per_p = res[2]
    
    select_cat = 'Category'
    select_city = 'Villes'

    querysetos = {}

    for every_it in res[0]:
        imo = PostImage.objects.filter(item=every_it)
        querysetos[every_it]=imo

    context = {
        'items': querysetos,
        'category':categorie,
        'cato':cato,
        'cato1':cato1,
        'cato2':cato2,
        'it_len':it_len,
        'page_request_var':res[1],
        'result_per_p' : result_per_p,
        'catos':catos,
        'villos':villos,
        'select_cat':select_cat,
        'select_city': select_city,
        'vi_len':vi_len,
    }

    return render(request, 'shop.html', context)


def productsPageDetail(request, arg, args):
    if args == 'Villes':
        #print(arg)
        print(args)

        items = []
        items_len = {}
        villos = {}
        vi_len = 0

        categorie = Category.objects.get(name_category=arg)
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        cato=False
        cato1 = True
        cato2 = False
        
        subcategory = Subcategory.objects.filter(category=categorie)
        
        for subcat in subcategory:
            item = Item.objects.filter(category=subcat)
            items_len[subcat]=len(item)
            #items_len.append(len(item))
            for it in item:
                items.append(it)

        len_it_found = len(items)
        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)

        if len_it_found< res[2]:
            result_per_p = len_it_found
        else:
            result_per_p = res[2]

        select_cat = arg
        select_city = args

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo

        context = {
            'items': querysetos,
            'items_len':items_len,
            'it_len':len_it_found,
            'category':categorie,
            'subcategory':subcategory,
            'cato':cato,
            'cato1':cato1,
            'cato2':cato2,
            'page_request_var':res[1],
            'villes':villes,
            'result_per_p' : result_per_p,
            'villos':villos,
            'select_cat':select_cat,
            'select_city':select_city,
            'vi_len':vi_len,
        }
    
    else:
        print(args)

        items = []
        items_len = {}
        villos = {}
        vi_len = 0

        categorie = Category.objects.get(name_category=arg)
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        cato=False
        cato1 = True
        cato2 = False
        
        subcategory = Subcategory.objects.filter(category=categorie)
        
        for subcat in subcategory:
            item = Item.objects.filter(category=subcat, location__icontains=args)
            items_len[subcat]=len(item)
            #items_len.append(len(item))
            for it in item:
                items.append(it)


        len_it_found = len(items)
        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)

        if len_it_found< res[2]:
            result_per_p = len_it_found
        else:
            result_per_p = res[2]

        select_cat = arg
        select_city = args

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo

        context = {
            'items': querysetos,
            'category':categorie,
            'cato':cato,
            'cato1':cato1,
            'cato2':cato2,
            'page_request_var':res[1],
            'result_per_p' : result_per_p,
            'villos':villos,
            'select_cat':select_cat,
            'select_city': select_city,
            'vi_len':vi_len,
            'items_len':items_len,
            'it_len':len_it_found,
        }


    return render(request, 'shop.html', context)


def productsPageSubDetail(request, argu, args):
    if args == 'Villes':
        print(args)
        #print(argu)
        villos = {}
        vi_len = 0
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)


        items=[]
        items_cat = []

        cato=False
        cato1=False
        cato2=True
        
        subcategory = Subcategory.objects.get(name_subcategory=argu)

        categorie = subcategory.category


        item = Item.objects.filter(category=subcategory)
        for it in item:
            items.append(it)

        it_nums = len(items)
        len_it_found = len(items)
        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_nums< res[2]:
            result_per_p = it_nums
        else:
            result_per_p = res[2]

        select_cat = argu
        select_city = args

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo

        context = {
            'items': querysetos,
            'category':categorie,
            'subcategory':argu,
            'cato':cato,
            'cato1':cato1,
            'cato2':cato2,
            'it_len':it_nums,
            'page_request_var':res[1],
            'result_per_p' : result_per_p,
            'cat_len': len_it_found,
            'villos':villos,
            'select_cat':select_cat,
            'select_city':select_city,
            'vi_len':vi_len,
        }

    else:
        print(args)
        #print(argu)
        villos = {}
        vi_len = 0
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)


        items=[]
        items_cat = []

        cato=False
        cato1=False
        cato2=True
        
        subcategory = Subcategory.objects.get(name_subcategory=argu)

        categorie = subcategory.category

        item = Item.objects.filter(category=subcategory, location__icontains=args)
        for it in item:
            items.append(it)

        it_nums = len(items)
        len_it_found = len(items)
        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_nums< res[2]:
            result_per_p = it_nums
        else:
            result_per_p = res[2]

        select_cat = argu
        select_city = args

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo

        context = {
            'items': querysetos,
            'category':categorie,
            'subcategory':argu,
            'cato':cato,
            'cato1':cato1,
            'cato2':cato2,
            'it_len':it_nums,
            'page_request_var':res[1],
            'result_per_p' : result_per_p,
            'cat_len': len_it_found,
            'villos':villos,
            'select_cat':select_cat,
            'select_city':select_city,
            'vi_len':vi_len,
        }

    return render(request, 'shop.html', context)

############# LES VILLES ##################
def villes(request, arg, args):
    if args == 'Category':

        print(arg)
        print(args)

        it_len = 0
        catos = {}
        villos = {}
        vi_len = 0
        categorie = Category.objects.all()


        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        items = Item.objects.filter(location__icontains = arg)
        it_len = len(items)

        for every_cat in categorie:
            subcategory=Subcategory.objects.filter(category=every_cat)
            cat_len = 0
            for every_sub_cat in subcategory:
                item = Item.objects.filter(category=every_sub_cat, location__icontains=arg)
                cat_len = cat_len+len(item)
                

            catos[every_cat] = cat_len
            

        cato=True
        cato1 = False
        cato2 = False

        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_len< res[2]:
            result_per_p = it_len
        else:
            result_per_p = res[2]
    
        select_cat = args
        select_city = arg

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo

        context = {
        'items': querysetos,
        'category':categorie,
        'cato':cato,
        'cato1':cato1,
        'cato2':cato2,
        'it_len':it_len,
        'page_request_var':res[1],
        'result_per_p' : result_per_p,
        'catos':catos,
        'villos':villos,
        'select_cat':select_cat,
        'select_city':select_city,
        'vi_len':vi_len,
        }
    else:
        try:
        
            print('YEEEEEEEEEERRRRRRRRRPPPPPPP')
            items = []
            items_len = {}
            villos = {}
            vi_len = 0

            

            cato=False
            cato1 = True
            cato2 = False
            
            subcat = Subcategory.objects.get(name_subcategory=args)
            item = Item.objects.filter(category=subcat, location__icontains=arg)
            items_len[subcat]=len(item)
            #items_len.append(len(item))
            for it in item:
                items.append(it)

            villes = Ville.objects.all()
            for vi in villes:
                it = Item.objects.filter(location__icontains = vi)
                villos[vi]=len(it)
                vi_len = vi_len+len(it)

            categorie = subcat.category

            len_it_found = len(items)
            itemss = order_by_cash(items, request)

            res = paginatora(request, itemss)

            if len_it_found< res[2]:
                result_per_p = len_it_found
            else:
                result_per_p = res[2]

            select_cat = args
            select_city = arg

            querysetos = {}

            for every_it in res[0]:
                imo = PostImage.objects.filter(item=every_it)
                querysetos[every_it]=imo

            context = {
                'items': querysetos,
                'category':categorie,
                'cato':cato,
                'cato1':cato1,
                'cato2':cato2,
                'page_request_var':res[1],
                'result_per_p' : result_per_p,
                'villos':villos,
                'select_cat':select_cat,
                'select_city': select_city,
                'vi_len':vi_len,
                'items_len':items_len,
                'it_len':len_it_found,
            }
        
        except:
            
            items = []
            items_len = {}
            villos = {}
            vi_len = 0

            categorie = Category.objects.get(name_category=args)
            

            cato=False
            cato1 = True
            cato2 = False
            
            subcategory = Subcategory.objects.filter(category=categorie)

            villes = Ville.objects.all()
            for vi in villes:
                it = Item.objects.filter(location__icontains = vi)
                villos[vi]=len(it)
                vi_len = vi_len+len(it)
            
            for subcat in subcategory:
                item = Item.objects.filter(category=subcat, location__icontains=arg)
                items_len[subcat]=len(item)
                #items_len.append(len(item))
                for it in item:
                    items.append(it)


            len_it_found = len(items)
            itemss = order_by_cash(items, request)

            res = paginatora(request, itemss)

            if len_it_found< res[2]:
                result_per_p = len_it_found
            else:
                result_per_p = res[2]

            select_cat = args
            select_city = arg

            querysetos = {}

            for every_it in res[0]:
                imo = PostImage.objects.filter(item=every_it)
                querysetos[every_it]=imo

            context = {
                'items': querysetos,
                'category':categorie,
                'cato':cato,
                'cato1':cato1,
                'cato2':cato2,
                'page_request_var':res[1],
                'result_per_p' : result_per_p,
                'villos':villos,
                'select_cat':select_cat,
                'select_city': select_city,
                'vi_len':vi_len,
                'items_len':items_len,
                'it_len':len_it_found,
            }

    return render(request, 'shop.html', context)








########### ALL CATEGORY ##############
def tous_category(request, args):
    if args == 'Villes':
        items = Item.objects.all()
        it_len = 0
        catos = {}
        villos = {}
        vi_len = 0

        categorie = Category.objects.all()
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        for every_cat in categorie:
            subcategory=Subcategory.objects.filter(category=every_cat)
            cat_len = 0
            for every_sub_cat in subcategory:
                item = Item.objects.filter(category=every_sub_cat)
                cat_len = cat_len+len(item)
                it_len = it_len+len(item)

            catos[every_cat] = cat_len
            

        cato=True
        cato1 = False
        cato2 = False

        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_len< res[2]:
            result_per_p = it_len
        else:
            result_per_p = res[2]
        
        select_cat = 'Category'
        select_city = 'Villes'

    else:
        it_len = 0
        catos = {}
        villos = {}
        vi_len = 0
        categorie = Category.objects.all()

        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        items = Item.objects.filter(location__icontains = args)
        it_len = len(items)

        for every_cat in categorie:
            subcategory=Subcategory.objects.filter(category=every_cat)
            cat_len = 0
            for every_sub_cat in subcategory:
                item = Item.objects.filter(category=every_sub_cat, location__icontains=args)
                cat_len = cat_len+len(item)
                

            catos[every_cat] = cat_len
            

        cato=True
        cato1 = False
        cato2 = False

        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_len< res[2]:
            result_per_p = it_len
        else:
            result_per_p = res[2]

        select_cat = 'Category'
        select_city = args


    querysetos = {}

    for every_it in res[0]:
        imo = PostImage.objects.filter(item=every_it)
        querysetos[every_it]=imo

    context = {
        'items': querysetos,
        'category':categorie,
        'cato':cato,
        'cato1':cato1,
        'cato2':cato2,
        'it_len':it_len,
        'page_request_var':res[1],
        'result_per_p' : result_per_p,
        'catos':catos,
        'villos':villos,
        'select_cat':select_cat,
        'select_city': select_city,
        'vi_len':vi_len,
    }

    return render(request, 'shop.html', context)





########### ALL CITY ##############
def tous_villes(request, args):
    if args == 'Category':
        items = Item.objects.all()
        it_len = 0
        vi_len = 0
        catos = {}
        villos = {}

        categorie = Category.objects.all()
        villes = Ville.objects.all()
        for vi in villes:
            it = Item.objects.filter(location__icontains = vi)
            villos[vi]=len(it)
            vi_len = vi_len+len(it)

        for every_cat in categorie:
            subcategory=Subcategory.objects.filter(category=every_cat)
            cat_len = 0
            for every_sub_cat in subcategory:
                item = Item.objects.filter(category=every_sub_cat)
                cat_len = cat_len+len(item)
                it_len = it_len+len(item)

            catos[every_cat] = cat_len
            

        cato=True
        cato1 = False
        cato2 = False

        itemss = order_by_cash(items, request)

        res = paginatora(request, itemss)
        if it_len< res[2]:
            result_per_p = it_len
        else:
            result_per_p = res[2]
        
        select_cat = 'Category'
        select_city = 'Villes'

        querysetos = {}

        for every_it in res[0]:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo


        context = {
        'items': querysetos,
        'category':categorie,
        'cato':cato,
        'cato1':cato1,
        'cato2':cato2,
        'it_len':it_len,
        'page_request_var':res[1],
        'result_per_p' : result_per_p,
        'catos':catos,
        'villos':villos,
        'select_cat':select_cat,
        'select_city': select_city,
        'vi_len':vi_len,
        }

    else:
        try:
        
            print('YEEEEEEEEEERRRRRRRRRPPPPPPP')
            items = []
            items_len = {}
            villos = {}
            vi_len = 0

            

            cato=False
            cato1 = True
            cato2 = False
            
            subcat = Subcategory.objects.get(name_subcategory=args)
            item = Item.objects.filter(category=subcat)
            items_len[subcat]=len(item)
            #items_len.append(len(item))
            for it in item:
                items.append(it)

            villes = Ville.objects.all()
            for vi in villes:
                it = Item.objects.filter(location__icontains = vi, category=subcat)
                villos[vi]=len(it)
                vi_len = vi_len+len(it)

            categorie = subcat.category

            len_it_found = len(items)
            itemss = order_by_cash(items, request)

            res = paginatora(request, itemss)

            if len_it_found< res[2]:
                result_per_p = len_it_found
            else:
                result_per_p = res[2]

            select_cat = args
            select_city = 'Villes'

            querysetos = {}

            for every_it in res[0]:
                imo = PostImage.objects.filter(item=every_it)
                querysetos[every_it]=imo

            context = {
                'items': querysetos,
                'category':categorie,
                'cato':cato,
                'cato1':cato1,
                'cato2':cato2,
                'page_request_var':res[1],
                'result_per_p' : result_per_p,
                'villos':villos,
                'select_cat':select_cat,
                'select_city': select_city,
                'vi_len':vi_len,
                'items_len':items_len,
                'it_len':len_it_found,
            }
        
        except:
            
            items = []
            items_len = {}
            villos = {}
            vi_len = 0

            categorie = Category.objects.get(name_category=args)
            

            cato=False
            cato1 = True
            cato2 = False
            
            subcategory = Subcategory.objects.filter(category=categorie)
            villes = Ville.objects.all()

            for vi in villes:
                it = Item.objects.filter(location__icontains = vi)
                villos[vi]=len(it)
                vi_len = vi_len+len(it)
            
            for subcat in subcategory:
                item = Item.objects.filter(category=subcat)
                items_len[subcat]=len(item)
                #items_len.append(len(item))
                for it in item:
                    items.append(it)


            len_it_found = len(items)
            itemss = order_by_cash(items, request)

            res = paginatora(request, itemss)

            if len_it_found< res[2]:
                result_per_p = len_it_found
            else:
                result_per_p = res[2]

            select_cat = args
            select_city = 'Villes'

            querysetos = {}

            for every_it in res[0]:
                imo = PostImage.objects.filter(item=every_it)
                querysetos[every_it]=imo

            context = {
                'items': querysetos,
                'category':categorie,
                'cato':cato,
                'cato1':cato1,
                'cato2':cato2,
                'page_request_var':res[1],
                'result_per_p' : result_per_p,
                'villos':villos,
                'select_cat':select_cat,
                'select_city': select_city,
                'vi_len':vi_len,
                'items_len':items_len,
                'it_len':len_it_found,
            }

    return render(request, 'shop.html', context)





########### PRODUCT DETAIL ############
def product_detail(request, slug):

    try:

        item_detail = get_object_or_404(Item, slug=slug)
        sub_cat=Subcategory.objects.get(name_subcategory=item_detail.category)

        photos = PostImage.objects.filter(item=item_detail)

        username = UserName.objects.filter(user=item_detail.user)
        username_uno = username[0]

        

        if item_detail.user.username == request.user.username:
            yerp = True
        else:
            yerp = False

        '''
        #Whatsapp number
        c_n = item_detail.whatsapp_number
        numbo = ''
        for every_el in c_n:
            if every_el=='[' or every_el==' ' or every_el==',' or every_el==']':
                continue
            else:
                numbo= numbo+every_el

        a = numbo.replace('(', '').replace(')', '')

        int_whatsapp_numbo = int(a)


        #phone number
        c_n = item_detail.call_number
        c_c = c_n.split(',')[0]
        co_n = c_n.split(',')[1]

        country_c = c_c.replace('(', '')
        country_n = co_n.replace(')', '')

        #print(country_c)
        #print(country_n)

        complete_call_numbo = '+'+country_c + country_n
        '''

        querysetos = {}

        related_products = Item.objects.filter(category=sub_cat).order_by('-timestamp')[0:4]
        for every_it in related_products:
            imo = PostImage.objects.filter(item=every_it)
            querysetos[every_it]=imo
        
        context = {
            'item_detail': item_detail,
            'sub_cat':sub_cat,
            'cat':sub_cat.category,
            #'item_color_variations':item_color_variations,
            #'item_size_variations':item_size_variations,
            'photos': photos,
            #'int_whatsapp_numbo':int_whatsapp_numbo,
            #'complete_call_numbo':complete_call_numbo,
            'related_products':related_products,
            'querysetos':querysetos,
            'usernamo':username_uno,
            'yerp':yerp,
            #'variation':variation,
        }

        return render(request, 'product-detail.html', context)
    
    except:
        redirect('shop-home')
        return render(request, 'index.html')

######## ORDER SUMMARY ###########

######## IS VALID FORM ##########
def is_valid_form(values):
    valid = True
    for value in values:
        if value=='':
            valid=False

    return valid
    



##CHOICES
'''
from itertools import accumulate as _accumulate, repeat as _repeat
from bisect import bisect as _bisect
import random
def choices(population, weights=None, *, cum_weights=None, k=1):
    """Return a k sized list of population elements chosen with replacement.
    If the relative weights or cumulative weights are not specified,
    the selections are made with equal probability.
    """
    n = len(population)
    if cum_weights is None:
        if weights is None:
            _int = int
            n += 0.0    # convert to float for a small speed improvement
            return [population[_int(random.random() * n)] for i in _repeat(None, k)]
        cum_weights = list(_accumulate(weights))
    elif weights is not None:
        raise TypeError('Cannot specify both weights and cumulative weights')
    if len(cum_weights) != n:
        raise ValueError('The number of weights does not match the population')
    bisect = _bisect
    total = cum_weights[-1] + 0.0   # convert to float
    hi = n - 1
    return [population[bisect(cum_weights, random.random() * total, 0, hi)]
            for i in _repeat(None, k)]
'''


########## CREAT SLUG CODE ###############
def create_slug_code():

    #return ''.join(choices(string.ascii_lowercase + string.digits, k=15))

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))


########## SELL PRODUCT #################
def sellProduct(request, args):
    #print(args)
    #print(args1)
    title = 'Vendre'
    form = SellPostForm(request.POST or None, request.FILES or None)
    #form1 = CountryNumberForm(request.POST or None, request.FILES or None)
    #form2 = CountryWhatsappNumberForm(request.POST or None, request.FILES or None)
    author = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = author
            form.instance.slug = create_slug_code()

            #category=
            sub_cat=Subcategory.objects.get(name_subcategory=args)
            form.instance.category = sub_cat

            #call_number
            '''
            number = form1.cleaned_data.get('country_number')
            code = form1.cleaned_data.get('number_country')

            x_call_number = phonenumbers.parse(number, code)
            print(x_call_number)
            '''

            #whatsapp_number
            '''
            number1 = form2.cleaned_data.get('country_number1')
            code1 = form2.cleaned_data.get('number_country1')

            x_whatsapp_number = phonenumbers.parse(number1, code1)
            print(x_whatsapp_number)
            '''

            '''
            form.instance.call_number = x_call_number.country_code, x_call_number.national_number
            form.instance.whatsapp_number = x_whatsapp_number.country_code, x_whatsapp_number.national_number
            '''

            form.save()

            slug = form.instance.slug

            items = Item.objects.filter(user=author)

            items_user = MyAccount(
                user = request.user,
            )

            items_user.save()
            items_user.item.set(items)

            return redirect('photo-product', slug=slug)

    context = {
        'title':title,
        'form':form,
    }

    return render(request, 'sell.html', context)

############ UPDATE PRODUCT ACCOUNT ###########
def updateProduct(request, slug, args):
    title = 'Update'
    item = get_object_or_404(Item, slug=slug)

    form = SellPostForm(request.POST or None, request.FILES or None, instance=item)

    author = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = author

            #category=
            sub_cat=Subcategory.objects.get(name_subcategory=args)
            form.instance.category = sub_cat


            form.save()

            return redirect('photo-product', slug=slug)

    context = {
        'title': title,
        'form':form,
    }
    return render(request, 'sell.html', context)

### Only the product, we do not modify the category
def updateProductOnly(request, slug):
    title = 'Update'
    item = get_object_or_404(Item, slug=slug)

    form = SellPostForm(request.POST or None, request.FILES or None, instance=item)

    author = request.user
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = author

            form.save()

            return redirect('photo-product', slug=slug)

    context = {
        'title': title,
        'form':form,
    }
    return render(request, 'sell.html', context)

############# DELETE PRODUCT ###############
def deleteProduct(request, slug):
    item = get_object_or_404(Item, slug=slug)
    item.delete()
    return redirect('me-account')

############ IMAGE UPLOAD ##############
def imagesUpload(request, slug):
    title = "Ajoutez d'autres images du produit"
    item = get_object_or_404(Item, slug=slug)
    form = PhotoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            for file in request.FILES.getlist('images')[:3]:
                instance = PostImage(
                    item=item,
                    image=file
                )
                instance.save()
            return redirect('product-detail', slug=slug)

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'imgs.html', context)


############## VARIATIONS UPLOAD #############

############## CHOOSE CATEGORY ########################
@login_required
def chooseCategory(request):
    categories = Category.objects.all()

    update = False
    sell = True

    context = {
        'categories':categories,
        'update':update,
        'sell':sell,
    }

    return render(request, 'categories.html', context)

############## CHOOSE CATEGORY UPDATE ########################

def chooseCategoryUpdate(request, slug):
    categories = Category.objects.all()
    it_slug = slug

    update = True
    sell = False

    context = {
        'categories':categories,
        'update':update,
        'sell':sell,
        'it_slug':it_slug
    }

    return render(request, 'categories.html', context)

############ CHOOSE SUBCATEGORY ######################
def chooseSubcategory(request, argum):
    categories = Category.objects.all()
    print(argum)
    categorie = Category.objects.get(name_category=argum)
    subcategorie = Subcategory.objects.filter(category=categorie)
    
    update = False
    sell = True

    context={
        'categories':categories,
        'subcategorie':subcategorie,
        'update':update,
        'sell':sell,
    }

    return render(request, 'categories.html', context)

############ CHOOSE SUBCATEGORY UPDATE ######################
def chooseSubcategoryUpdate(request, argum, slug):
    categories = Category.objects.all()
    print(argum)
    print(slug)
    categorie = Category.objects.get(name_category=argum)
    subcategorie = Subcategory.objects.filter(category=categorie)
    
    it_slug = slug

    update = True
    sell = False

    context={
        'categories':categories,
        'subcategorie':subcategorie,
        'update':update,
        'sell':sell,
        'it_slug':it_slug,
    }

    return render(request, 'categories.html', context)


def changeUserName(request):
    form = UserNamePostForm(request.POST or None)
    author = request.user
    
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = author
            form.save()

            return redirect('me-account')

    context = {
        'form':form,
    }

    return render(request, 'username.html', context)