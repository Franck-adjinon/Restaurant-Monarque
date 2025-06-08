from pyexpat.errors import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import (
    Chef,
    Liensociale,
    Menu,
    Plat,
    Service_client,
    Email_send,
    Newsletter_email,
    Contact_company,
    Studio_info,
    Liensociale_company,
    Article,
)
from .task import send_email_in_background_template
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.template import loader

# *Import generic views
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.utils.timezone import now
from django.shortcuts import redirect, render

# * pour la pagination
from django.core.paginator import Paginator

# * les formulaires
from .forms import MessageForm

# *gestion des logs
import logging 
# Obtenir un logger nommé selon le nom du module courant
logger = logging.getLogger(__name__)


# TODO: Affiche la page d'accueil
def index(request):
    # initialisation par défaut
    plat_epingler = []
    menu_epingler = []
    chef_epingler = []
    liste_article = []
    lien_map = []
    contacts = []
    liens = [] 

    # Récupérer tout les plats épingler
    try:
        plat_epingler = Plat.objects.filter(pinned=True, actif=True).order_by(
            "-date_creation"
        )[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des plats épingler")

    # Récupérer tout les menus épingler
    try:
        menu_epingler = Menu.objects.filter(pinned=True, actif=True).order_by(
            "-date_creation"
        )[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des menus épingler")

    # Récupérer tout les chefs épingler
    try:
        chef_epingler = Chef.objects.filter(actif=True).order_by("-date_creation")[:4]
        for chef in chef_epingler:
            # Ajout d'un attribut d’instance dynamique (liens)
            chef.liens = chef.liensociale_set.order_by(
                "designation"
            )  # lien associé au chefs
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des chefs épingler")

    # Récupérer tout les articles
    try:
        liste_article = Article.objects.filter(status=True).order_by("-date_creation")[
            :4
        ]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des articles")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération du lien map du restaurant")

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Gestion du formulaire
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            email = form.cleaned_data["email"]
            sujet = form.cleaned_data["sujet"]
            message = form.cleaned_data["message"]
            try:
                # * Avec le template personnalisé
                send_email_in_background_template(sujet, message, email, nom)
            except BadHeaderError:
                return HttpResponse("En-tête non valide trouvé.")
            # redirect vers la page de remerciement
            return redirect("message_thanks")
    else:
        form = MessageForm()

    return render(
        request,
        "index.html",
        {
            "plat_epingler": plat_epingler,
            "menu_epingler": menu_epingler,
            "chef_epingler": chef_epingler,
            "liste_article": liste_article,
            "lien_map": lien_map,
            "contacts": contacts,
            "liens": liens,
            "form": form,
        },
    )


# TODO: Affiche la page des plats
def plats(request):
    # initialisation par défaut
    page_obj = [] 
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les plats
    try:
        plats_actif = Plat.objects.filter(actif=True).order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des plats actif")

    paginator = Paginator(plats_actif, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    return render(
        request,
        "plats.html",
        {
            "page_obj": page_obj,
            "contacts": contacts,
            "lien_map": lien_map,
            "liens": liens,
        },
    )


# TODO: Affiche la page des menus
def menus(request):
    # initialisation par défaut
    page_obj = []
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les menus
    try:
        menus_actif = Menu.objects.filter(actif=True).order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des menus actif")

    paginator = Paginator(menus_actif, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    return render(
        request,
        "menus.html",
        {
            "page_obj": page_obj,
            "contacts": contacts,
            "lien_map": lien_map,
            "liens": liens,
        },
    )


# TODO: Affiche la page des chefs
def chefs(request):  
    # initialisation par défaut
    chefs_actif = []
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les chefs
    try:
        chefs_actif = Chef.objects.filter(actif=True).order_by("-date_creation")
        for chef in chefs_actif:
            # Ajout d'un attribut d’instance dynamique (liens)
            chef.liens = chef.liensociale_set.order_by(
                "designation"
            )  # lien associé au chefs
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des chefs actif")

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    return render(
        request,
        "chefs.html",
        {
            "chefs_actif": chefs_actif,
            "contacts": contacts,
            "lien_map": lien_map,
            "liens": liens,
        },
    )


# TODO: Affiche la page les articles
def blog(request):
    # initialisation par défaut
    page_obj = []
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les articles
    try:
        article_actif = Article.objects.filter(status=True).order_by("-date_creation")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des articles actif")

    paginator = Paginator(article_actif, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    return render(
        request,
        "Blogs.html",
        {
            "page_obj": page_obj,
            "contacts": contacts,
            "lien_map": lien_map,
            "liens": liens,
        },
    )


# TODO: Afficher l'article avec ses informations
def article_details(request, slug):
    template = loader.get_template("article.html")

    # initialisation par défaut
    article = []
    article_con = []
    lien_map = []
    contacts = []
    liens = []

    # On récupère l'article avec le slug
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        logger.error("Aucune information retournée pour le slug")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération de l'article")

    # Récupérer les articles pour le carroussel
    try:
        article_con = (
            Article.objects.exclude(slug=slug)
            .order_by("-date_creation")
            .filter(status=True)[:4]
        )
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des articles pour le carrousel")

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    context = {
        "article_con": article_con,
        "article": article,
        "contacts": contacts,
        "lien_map": lien_map,
        "liens": liens,
    }
    return HttpResponse(template.render(context, request))


# TODO: Afficher le menu avec ses informations
def menu_details(request, nom):
    template = loader.get_template("single_menus.html")

    # initialisation par défaut
    menu = []
    menu_con = []
    menu_plats = []
    lien_map = []
    contacts = []
    liens = []

    # On récupère le menu avec le nom
    try:
        menu = Menu.objects.get(nom=nom)
    except Menu.DoesNotExist:
        logger.error("Aucune information retournée pour le nom")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération du menu")

    # Récupérer les menus pour le carroussel
    try:
        menu_con = Menu.objects.exclude(nom=nom, actif=False).order_by(
            "-date_creation"
        )[:3]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des menu du carroussel")

    # Récupérer les plats du menu
    try:
        menu_plats = menu.plat_set.all()
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des plats du menu")

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    context = {
        "menu": menu,
        "menu_con": menu_con,
        "menu_plats": menu_plats,
        "contacts": contacts,
        "lien_map": lien_map,
        "liens": liens,
    }
    return HttpResponse(template.render(context, request))


# TODO: Afficher le plat avec ses informations
def plat_details(request, nom):
    template = loader.get_template("single_plats.html")

    # initialisation par défaut
    plat = []
    plat_con = [] 
    lien_map = []
    contacts = []
    liens = []

    # On récupère le plat avec le nom
    try:
        plat = Plat.objects.get(nom=nom)
    except Plat.DoesNotExist:
        logger.error("Aucune information retournée pour le nom")
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération du menu")

    # Récupérer les plats pour le carroussel
    try:
        plat_con = Plat.objects.exclude(nom=nom, actif=False).order_by(
            "-date_creation"
        )[:3]
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération des plats pour le carroussel"
        )

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    context = {
        "plat": plat,
        "plat_con": plat_con,
        "contacts": contacts,
        "lien_map": lien_map,
        "liens": liens,
    }
    return HttpResponse(template.render(context, request))


# TODO: Afficher la page de remercienement après envoie de message du client vers restaurant
def message_thanks(request):
    template = loader.get_template("form_thanks.html")

    # initialisation par défaut
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    context = {"contacts": contacts, "lien_map": lien_map, "liens": liens}
    return HttpResponse(template.render(context, request))


# TODO: Afficher la page de remercienement après inscription à la newsletter
def news_thanks(request):
    template = loader.get_template("news_thanks.html")

    # initialisation par défaut
    lien_map = []
    contacts = []
    liens = []

    # Récupérer les contact du restaurant
    try:
        contacts = Contact_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des contact")

    # Récupérer les liens vers les comptes du restaurant
    try:
        liens = Liensociale_company.objects.all()[:4]
    except Exception as e:
        logger.error("Erreur inattendue lors de la récupération des liens")

    # Récupérer le lien map du restaurant
    try:
        lien_map = Studio_info.objects.latest("-date_creation")
    except Studio_info.DoesNotExist:
        logger.error("Aucune information retournée pour le lien map du restaurant")
    except Exception as e:
        logger.error(
            "Erreur inattendue lors de la récupération du lien map du restaurant"
        )

    context = {"contacts": contacts, "lien_map": lien_map, "liens": liens}
    return HttpResponse(template.render(context, request))


# TODO: Pour s'ajouter à le visiteur à la newsletter
def add_newsletter(request):
    from_email = request.POST.get("from_email", "")
    if from_email:
        try:
            # * Sauvegarder l'email
            Newsletter_email.objects.create(email_visteur=from_email, actif=True)
        except BadHeaderError:
            return HttpResponse("En-tête non valide trouvé.")
        return redirect("news_thanks")
    else:
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
