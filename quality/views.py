# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView
from  django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from bootstrap_modal_forms.mixins import LoginAjaxMixin, PassRequestMixin
from .methods import query_off, best_substitut
from .models import SubstitutProduct, Backup, Product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
import re

def accueil(request):
    return render(request, 'quality/index.html')

def credits(request):
    return render(request, 'quality/credits.html')


def query_data(request):
    ''' we retrieve the user input: 'query'
    if there are no results
    we query the OFF API : 'query_off' methods.py
    and we display useful data '''

    query = request.GET.get('query', None)

    if not query:
        title = "saisissez un produit ! "
        context = {'title': title }
        return render(request, 'quality/index.html', context)

    else:

        title = 'Votre recherche est :  "{}"  . '.format(query)

        # we ask quality database
        data_quality = Product.objects.filter(name__icontains=query)[:6]
        if len(data_quality) == 6:
            context = {
                'title': title ,
                'data_quality': data_quality
            }
            return render(request , 'quality/query_data.html' , context)

        # if we don't have enough product in database : we ask OpenFood Facts
        if len(data_quality) <= 6:

            # query_off function calls OFF API and return 6 products

            data_off = query_off(query)

            # in case of invalid user entry
            if not data_off:
                title = 'Votre recherche "{}" n \' a donné aucun resultat!'.format(query)
                context = {'title': title}
                return render(request, 'quality/index.html', context)

            else:
                # we provide a choice among 6 products
                l = 6 - len(data_quality)
                data_off = data_off[:l]
                context = {
                    'title': title ,
                    'data_quality': data_quality,
                    'data_off': data_off
                }
                return render(request, 'quality/query_data.html', context)

# return render(request , 'quality/query_data.html' , context)

def sub_product(request):
    '''recovery of the selected product
    recording data in the session
    category recovery
    interrogation of the OFF api and display of the 6 best substitute products: via best_substitute methods.py '''

    # get the user choice from the checkbox

    choices = request.GET.get('subscribe', None)

    # split the checkbox's return in order to make a python list

    choices = choices.split(', ')

    # record selected product in session

    record_session = ['selected_name', 'selected_category', 'selected_img', 'selected_nutriscore', 'selected_url']
    for value , choice in zip(record_session , choices):
        request.session[value] = choice

    cat = request.session['selected_category']
    name = request.session['selected_name']

    # we query in database three best product
    data_quality = Product.objects.filter(category=cat).exclude(name=name).order_by('n_grade')[:6]

    # we query OpenFoodfacts three other best products with the same category

    data_off = best_substitut(cat)

    # we make sure to return a valid sample
    # total_length = 6 - len(data_quality)
    # data_off = data_off[:total_length]

    context = {
        'data_quality': data_quality,
        'data_off' : data_off
    }
    return render(request, 'quality/sub_product.html', context)

@login_required
def user_choice(request):
    '''View showing the pair of products saved.
     Registers data in the database.
     The substitute product is recorded in the session for display.'''
    # get the user choice from the checkbox
    choices = request.GET.get('subscribe', None)

    # split the checkbox's return in order to make a python list
    choices = choices.split(', ')

    # check if selected product is already in database with the url entry
    try:
        p_selected = Product.objects.get(url=request.session['selected_url'])
    except Product.DoesNotExist:
        # then we enrich the database
        # record selected product in database
        p_selected = Product.objects.create(
            name = request.session['selected_name'],
            url = request.session['selected_url'],
            img = request.session['selected_img'],
            n_grade = request.session['selected_nutriscore'],
            category = request.session['selected_category'])

    # check if substitut product is already in database with the url entry
    # if not we enrich the data_base
    try:
        p_substitut_reference = Product.objects.get(url=choices[4])
    except Product.DoesNotExist:
        p_substitut_reference = Product.objects.create(
            name=choices[0] ,
            category=choices[1] ,
            img=choices[2] ,
            n_grade=choices[3] ,
            url=choices[4] ,
            img_nutrition=choices[5] ,
            store=choices[6])


    # record the backup with selected_product_id and user_id
    backup = Backup.objects.create(
        user_id = request.user,
        selected_product_id = p_selected
    )

    # record the substitute product with all the foreign key
    p_substitut = SubstitutProduct.objects.create(
        name = choices[0],
        category = choices[1],
        img = choices[2],
        n_grade = choices[3],
        url = choices[4],
        img_nutrition = choices[5],
        store = choices[6],

        backup_id = backup,
        user_id = request.user,
        selected_product_id = p_selected
    )



    # record selected product in session just for display
    record_session = ['substitut_name', 'substitut_category', 'substitut_img', 'substitut_nutriscore', 'substitut_url']
    for value , choice in zip(record_session, choices):
        request.session[value] = choice
    return render(request, 'quality/user_choice.html')




@login_required
def myaccount(request):
    return render(request, 'quality/account.html')

@login_required
def food(request):
    '''View which display page of Aliments . firstly we are looking for the connected user,
    then we are looking for all backups related to this user, the display supports pagination'''

    #define the connected user
    user = request.user

    # request inner join on selectedproduct/Backup/substitutproduct
    sel_product_list = Product.objects.filter(backup__user_id=user.id).order_by('backup__id')
    sub_product_list = SubstitutProduct.objects.filter(user_id=user.id).order_by('id')
    # Slice pages
    paginator0 = Paginator(sel_product_list, 1)
    paginator1 = Paginator(sub_product_list, 1)
    # Get current page
    page = request.GET.get('page', 1)
    try:
        #return only the first product and not the others
        sel_products = paginator0.page(page)
        sub_products = paginator1.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        sel_products = paginator0.page(1)
        sub_products = paginator1.page(1)
    except EmptyPage:
        #If page out of range (e.g 99999), deliver last page of results.
        sel_products = paginator0.page(paginator0.num_pages)
        sub_products = paginator1.page(paginator1.num_pages)
    context = {
        'sel_products': sel_products,
        'sub_products': sub_products
    }

    return render(request, 'quality/food.html', context)



# Authentification views

class CustomLoginView(LoginAjaxMixin, SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'quality/registration/login.html'
    success_message = 'Vous etes à présent connecté'

class SignUpView(PassRequestMixin, SuccessMessageMixin, generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'quality/registration/signup.html'

    def get_success_url(self):
        #log user after register
        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            referer_url = self.request.META.get('HTTP_REFERER')
            messages.success(self.request, ('Création de compte réussie ! Vous etes à présent connecté !'))
            return referer_url


def logout_view(request):
    logout(request)
    messages.success(request, ('Vous etes déconnecté'))
    return redirect('quality:accueil')