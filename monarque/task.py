import threading
from django.core.mail import send_mail 
from .models import Service_client, Email_send, Newsletter_email
# *Pour la mise en place du template email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Fonction : mise en place du template email
def send_email_in_background_template(sujet, message, from_client, nom_client):
    def email_task(): 
        # Récuperer les agents du service clients actif
        Agents = Service_client.objects.filter(actif = True)
        # Créer une nouvelle instance de message envoyer au service client
        Email_send.objects.create(nom=nom_client, email=from_client, message=message)
        #
        html_content = render_to_string(
            "emails/new_client.html",
            {
                "nom_client": {"nom": nom_client},
                "email_client": {"email": from_client},
                "sujet": {"sujet": sujet},
                "message": {"message": message},
            },
        )
        text_content = strip_tags(html_content)  # Version texte brut
        for agent in Agents:
            email = EmailMultiAlternatives(
                subject=sujet,  # Sujet de l'e-mail 
                body=text_content,  # Corps du message (version texte brut)
                from_email=from_client,  # Adresse de l'expéditeur
                to=[agent.email],  # Adresse de l'agent du service client
            )
            email.attach_alternative(html_content, "text/html")
            email.send() 

    thread = threading.Thread(target=email_task)
    thread.start()


# Fonction : Envoyer les emails dynamiquement au abonner
def send_email_abonne(sujet, from_client, titre_article, contenu):
    def email_task(): 
        # Récuperer les abonnées à la newsletter actif
        abonner = Newsletter_email.objects.filter(actif = True) 
        # Mise en 
        html_content = render_to_string('emails/new_article.html', { 
            'title': {'title': titre_article},
            'article': {'content': contenu},
            'email_client': {'email': from_client}
        })
        text_content = strip_tags(html_content)  # Version texte brut
        for ab in abonner:
            email = EmailMultiAlternatives(
                subject=sujet,  # Sujet de l'e-mail 
                body=text_content,  # Corps du message (version texte brut)
                from_email=from_client,  # Adresse de l'expéditeur
                to=[ab.email_visteur],  # Adresse de l'abonner
            )
            email.attach_alternative(html_content, "text/html")
            email.send() 
    
    thread = threading.Thread(target=email_task)
    thread.start()
