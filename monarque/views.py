from django.urls import reverse_lazy  
from .models import Chef, Liensociale, Menu, Plat, Service_client, Email_send, Newsletter_email, Contact_company, Studio_info, Liensociale_company, Article
from django.http import HttpResponse
from django.template import loader
# *Import generic views
from django.views.generic.detail import DetailView 
from django.views.generic import View
from django.utils.timezone import now 
from django.shortcuts import render


# TODO: Affiche la page d'accueil
def index(request):  
    # Récupérer tout les plats épingler
    try:
        plat_epingler = Plat.objects.filter(pinned=True, actif=True).order_by('-date_creation')[:3]
    except Exception as e:
        pass
    
    
    # Récupérer tout les menus épingler
    try:
        menu_epingler = Menu.objects.filter(pinned=True, actif=True).order_by('-date_creation')[:4]
    except Exception as e:
        pass
    
    # Récupérer tout les chefs épingler
    try:
        chef_epingler = Chef.objects.filter(actif=True).order_by('-date_creation')[:4] 
        for chef in chef_epingler:
            # Ajout d'un attribut d’instance dynamique (liens)
            chef.liens = chef.liensociale_set.order_by('designation')  # lien associé au chefs  
    except Exception as e:
        pass 
    
    
    # Récupérer tout les articles 
    try:
        liste_article = Article.objects.filter(status=True).order_by('-date_creation')[:4]
    except Exception as e:
        pass
    
    
    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest('-date_creation')
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    return render(request, 'index.html', {
        'plat_epingler': plat_epingler, 
        'menu_epingler': menu_epingler, 
        'chef_epingler': chef_epingler, 
        'liste_article': liste_article, 
        'lien_map': lien_map,
        'contacts': contacts,
        'liens': liens 
        }) 


# TODO: Affiche la page des plats
def plats(request):   
    # Récupérer les plats
    try:
        plats_actif = Plat.objects.filter(actif=True).order_by('-date_creation')
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    return render(request, 'plats.html', { 
        'plats_actif': plats_actif,
        'contacts': contacts,
        'liens': liens 
        }) 


# TODO: Affiche la page des menus
def menus(request):   
    # Récupérer les menus
    try:
        menus_actif = Menu.objects.filter(actif=True).order_by('-date_creation')
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    return render(request, 'menus.html', { 
        'menus_actif': menus_actif,
        'contacts': contacts,
        'liens': liens 
        }) 


# TODO: Affiche la page des chefs
def chefs(request):   
    # Récupérer les chefs
    try:
        chefs_actif = Chef.objects.filter(actif=True).order_by('-date_creation')
        for chef in chefs_actif:
            # Ajout d'un attribut d’instance dynamique (liens)
            chef.liens = chef.liensociale_set.order_by('designation')  # lien associé au chefs  
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    return render(request, 'chefs.html', { 
        'chefs_actif': chefs_actif,
        'contacts': contacts,
        'liens': liens 
        }) 


# TODO: Affiche la page les articles
def blog(request):   
    # Récupérer les articles
    try:
        article_actif = Article.objects.filter(status=True).order_by('-date_creation') 
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    return render(request, 'Blogs.html', { 
        'article_actif': article_actif,
        'contacts': contacts,
        'liens': liens 
        }) 


# TODO: Afficher l'article avec ses informations
def article_details(request, slug):
    article = Article.objects.get(slug=slug) # On récupère l'article avec le slug
    template = loader.get_template('article.html')
    
    
    # Récupérer les articles pour le carroussel
    try:
        article_con = Article.objects.exclude(slug=slug).order_by('-date_creation').filter(status=True)[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    
    context = {
        'article_con': article_con,
        'article': article,
        'contacts': contacts,
        'liens': liens
    }
    return HttpResponse(template.render(context, request))


# TODO: Afficher le menu avec ses informations
def menu_details(request, nom):
    menu = Menu.objects.get(nom=nom) # On récupère le menu avec le slug
    template = loader.get_template('single_menus.html')
    
    
    # Récupérer les articles pour le carroussel
    try:
        menu_con = Menu.objects.exclude(nom=nom, actif=False).order_by('-date_creation')[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les plats du menu
    try:
        menu_plats = menu.plat_set.all()
    except Exception as e:
        pass
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    
    context = {
        'menu': menu,
        'menu_con': menu_con,
        'menu_plats': menu_plats,
        'contacts': contacts,
        'liens': liens
    }
    return HttpResponse(template.render(context, request))


# TODO: Afficher le plat avec ses informations
def plat_details(request, nom):
    plat = Plat.objects.get(nom=nom) # On récupère le plat avec le slug
    template = loader.get_template('single_plats.html')
    
    
    # Récupérer les plats pour le carroussel
    try:
        plat_con = Plat.objects.exclude(nom=nom, actif=False).order_by('-date_creation')[:4]
    except Exception as e:
        pass 
    
    
    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        pass
    
    
    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        pass 
    
    
    context = {
        'plat': plat,
        'plat_con': plat_con, 
        'contacts': contacts,
        'liens': liens
    }
    return HttpResponse(template.render(context, request))