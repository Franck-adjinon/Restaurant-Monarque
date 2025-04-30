from django.urls import path  
from django.conf import settings
from django.conf.urls.static import static
from . import views  

urlpatterns = [
    # TODO: Affiche la page d'accueil
    path('', views.index, name='index'), 
    
    # TODO: Affiche la page des plats
    path('plats', views.plats, name='plats'), 
    
    # TODO: Affiche la page des menus
    path('menus', views.menus, name='menus'), 
    
    # TODO: Affiche la page des chefs
    path('chefs', views.chefs, name='chefs'), 
    
    # TODO: Affiche la page les articles
    path('blog', views.blog, name='blog'), 
    
    # TODO: Afficher un article avec ses détails
    path('blog/article_detail/<slug:slug>', views.article_details, name='article_detail'),
    
    # TODO: Afficher un menu avec ses détails
    path('menus/menu_detail/<str:nom>', views.menu_details, name='menu_detail'),
    
    # TODO: Afficher un plat avec ses détails
    path('plats/plat_detail/<str:nom>', views.plat_details, name='plat_detail'),
    
    # TODO: Affiche la page de remercienement après envoie de message du client vers restaurant
    path('message_thanks', views.message_thanks, name='message_thanks'), 
    
    # TODO: Affiche la page de remercienement après inscription à la newsletter
    path('news_thanks', views.news_thanks, name='news_thanks'), 
    
    # TODO: Pour la gestion des envoie de mails
    path('send_mail', views.email_envoyer, name='send_mail'),
    
    # TODO: Pour s'ajouter à le visiteur à la newsletter
    path('subscribe_news', views.add_newsletter, name='subscribe_news'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)