from django.shortcuts import render
from .models import MyAccount
from shop.models import Item, UserName
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

########## PAGINATOR ###########
def paginatora(request, itemo):

    paginator = Paginator(itemo, 2)
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

    return result

####### ITEM ORDER BY ############
def order_by_cash(item, request):

    select_sort = request.GET.get('select_sort')
    if select_sort == 'Price: $$ - $':
        return item.order_by('-price')

    elif select_sort == 'Price: $ - $$':
        return item.order_by('price')

    else:
        return item

########## MY ACCOUNT ################
@login_required
def me_account(request):
    items = Item.objects.filter(user=request.user)
    username = UserName.objects.filter(user=request.user)

    if username:
        username_uno = username[0]
    else:
        username_uno = request.user.username

    '''
    items_user = MyAccount(
        user = request.user,
    )
    items_user.save()
    items_user.item.set(items)
    
    user_item = MyAccount.objects.all()
    '''
    it_len = len(items)
    itemss = order_by_cash(items, request)
    res = paginatora(request, itemss)

    print(res)

    context = {
        'item':itemss,
        'items':res[0],
        'it_len':it_len,
        'page_request_var':res[1],
        'usernamo':username_uno,
    }

    return render(request, 'me_account.html', context)

############# MY MEMBERSHIP ##################
def me_membership(request):
    return render(request, 'me_membership.html')

############## MY SETTINGS ###################
def me_settings(request):
    return render(request, 'me_settings.html')