from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from simple_history.models import HistoricalRecords
from django.db import models
import os
from dotenv import load_dotenv
# Charger les variables d'environnement
load_dotenv()

# service_client pour stocker les infos des agents qui prendront les message des clients
class Service_client(models.Model):
    id_agent = models.AutoField(primary_key=True)
    nom = models.CharField('Nom', max_length=50, unique=True)
    email = models.EmailField('Email', max_length=254, unique=True)
    actif = models.BooleanField('Agent actif ?', default=True)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.nom} {self.email}"

# newsletter_email pour stocker les emails donner par les visiteurs du site souhaitant recevoir des emails lors de nouvelles publication sur le blog
class Newsletter_email(models.Model):
    id_new = models.AutoField(primary_key=True)
    email_visteur = models.EmailField('Email visiteur', max_length=254, unique=True)
    actif = models.BooleanField('actif ?', default=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.email_visteur}"

# contact_company pour stocker les contacts du restaurant
class Contact_company(models.Model):
    id_contact = models.AutoField(primary_key=True)
    contact = models.CharField('Contact', max_length=50, unique=True)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.contact}"

# liensociale_company pour stocker les liens des comptes du restaurant sur les plateformes
class Liensociale_company(models.Model):
    id_lien = models.AutoField(primary_key=True)
    designation = models.CharField('Nom de la Plateforme', max_length=50)
    lien = models.CharField('lien vers le compte', max_length=255, unique=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.lien}"

# email_send pour stocker les mails envoyer au agents du service clients par les clients
class Email_send(models.Model):
    id_message = models.AutoField(primary_key=True)
    nom = models.CharField('Nom Client', max_length=50)
    email = models.EmailField('Email Client', max_length=254)
    message = models.CharField("Message du Client", max_length=255)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True) 
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.nom} {self.email}"

# studio_info pour stocker les informations du restaurant comme l'adresse maps
class Studio_info(models.Model):
    id_info = models.AutoField(primary_key=True)
    app_name = models.CharField('Nom Restaurant', max_length=50)
    app_adresse = models.CharField('Adresse Restaurant', max_length=50)
    app_mapslocation = models.TextField('Adresse Maps')
    app_mailadresse = models.EmailField('Email Restaurant', max_length=254)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True) 
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.app_name} {self.app_adresse}"

# article pour stocker les articles publier par le restaurant
class Article(models.Model):
    id_article = models.AutoField(primary_key=True)
    status = models.BooleanField('Publier ?', default=True)
    titre = models.CharField("Titre de l'article", max_length=150)
    slug = models.SlugField(default='' , null=False, max_length=150)
    lead = models.CharField("lead text", max_length=150)
    content = models.TextField('Contenu principal')
    cover = models.ImageField('Image de couverture', upload_to='Article_cover_image/')
    image = models.ImageField('Image principal', upload_to='Article_main_image/')
    cover_alt_text = models.CharField("Texte alternatif pour accessibilité de l'image de couverture", max_length=125)
    image_alt_text = models.CharField("Texte alternatif pour accessibilité de l'image principal", max_length=125) 
    date_creation = models.DateTimeField('Date Création', auto_now_add=True) 
    history = HistoricalRecords()
    
    
    def save(self, *args, **kwargs): 
        """Envoie un email à tout les abonner de la newsletter"""
        from .task import send_email_abonne 
        
        is_new = self._state.adding
        
        super().save(*args, **kwargs)
        
        if is_new:
            sujet =  "Nouvel article" 
            mail = os.getenv('EMAIL_HOST_USER') 
            titre = self.titre  
            texte = self.content[0:int(len(self.content)/2)] + "..."
            send_email_abonne(sujet= sujet, from_client=mail, titre_article=titre, contenu=texte) 
        
    
    
    def __str__(self):
        return f"{self.titre} {self.date_creation}"

# menu pour stocker les menu du restaurant
class Menu(models.Model):
    id_menu = models.AutoField(primary_key=True) 
    nom = models.CharField("Nom Menu", max_length=50) 
    description = models.CharField("Description", max_length=255) 
    image = models.ImageField('Image principal', upload_to='Menus_image/') 
    image_alt_text = models.CharField("Texte alternatif pour accessibilité de l'image principal", max_length=125) 
    actif = models.BooleanField('Visible ?', default=True)
    pinned = models.BooleanField('Épingler ?', default=True)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True) 
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80%

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom}"

# plat pour stocker les plats du restaurant
class Plat(models.Model):
    id_plat = models.AutoField(primary_key=True) 
    nom = models.CharField("Nom Plat", max_length=50) 
    description = models.TextField("Description") 
    image = models.ImageField('Image plat', upload_to='Plats_image/') 
    image_alt_text = models.CharField("Texte alternatif pour accessibilité de l'image", max_length=125) 
    actif = models.BooleanField('Visible ?', default=True)
    pinned = models.BooleanField("Épingler ?", default=True)
    date_creation = models.DateTimeField('Date Création', auto_now_add=True) 
    id_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80%

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom}"

# chef pour stocker les chefs du restaurant
class Chef(models.Model):
    id_chef = models.AutoField(primary_key=True) 
    nom = models.CharField("Nom Chef", max_length=50) 
    prenom = models.CharField("Prenom Chef", max_length=50) 
    specialite = models.CharField("Rôle", max_length=150)  
    image = models.ImageField('Image chef', upload_to='Chefs_image/') 
    image_alt_text = models.CharField("Texte alternatif pour accessibilité de l'image", max_length=125) 
    actif = models.BooleanField('Actif ?', default=True) 
    date_creation = models.DateTimeField('Date Création', auto_now_add=True)  
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")  # Assurer compatibilité
                img_io = BytesIO()

                # Toujours compresser l'image
                img.save(img_io, format="WEBP", quality=80)  # Ajuster la qualité 80%

                # Remplacer l'image originale par la version compressée
                new_image_name = f"{self.image.name.split('.')[0]}_compressed.webp"
                self.image = ContentFile(img_io.getvalue(), new_image_name)
            except Exception as e:
                raise ValueError(f"Erreur lors du traitement de l'image : {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

# liensociale pour stocker les liens sociales des chefs
class Liensociale(models.Model):
    id_lien = models.AutoField(primary_key=True)
    designation = models.CharField('Nom de la Plateforme', max_length=50)
    lien = models.CharField('lien vers le compte', max_length=255, unique=True)
    id_chef = models.ForeignKey(Chef, on_delete=models.CASCADE, default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.lien
