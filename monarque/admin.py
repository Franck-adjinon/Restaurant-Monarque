from django.contrib import admin
from django.contrib import admin as django_admin
# Import de 'admin' de unfold
from unfold.admin import ModelAdmin, StackedInline
# Import dans le cadre de la modification de l'interface d'ajout des users et groups de DJANGO admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
# For Nonrelated inlines
from unfold.contrib.inlines.admin import NonrelatedTabularInline, NonrelatedStackedInline
# Import pour la mise en place des filtres sur les models
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import(
        TextFilter, 
        FieldTextFilter,
        RangeDateFilter, 
        ChoicesDropdownFilter,
        MultipleChoicesDropdownFilter,
        RelatedDropdownFilter,
        MultipleRelatedDropdownFilter,
        DropdownFilter,
        MultipleDropdownFilter 
    )   
# Import pour améliorer la gestion du texte enrichi dans l'interface d'administration Django 
from unfold.contrib.forms.widgets import WysiwygWidget
# Récuperation des models
from .models import Chef, Liensociale, Menu, Plat, Service_client, Email_send, Newsletter_email, Contact_company, Studio_info, Liensociale_company, Article
from django.db import models

# unregister 
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# Pour afficher les liens sociale des chefs en tab inline
class liensocialeInline(StackedInline):
    model = Liensociale
    extra = 3
    tab = True  




# Les chefs
@admin.register(Chef)
class ChefAdmin(ModelAdmin):
    list_display = ('full_name', 'spec', 'status', 'create_date')  
    search_fields = ('nom','prenom',)             # Permet de rechercher par nom ou prenom 
    
    inlines = [liensocialeInline] # Possiblité d'ajouter en même temps les liens sociales du chef
    
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter = [ 
        ("date_creation", RangeDateFilter),
    ]  
    
    @admin.display(
        ordering="nom",
        description="Nom - Prenom",
    )
    def full_name(self, obj):
        return obj.nom + " " + obj.prenom
    
    @admin.display(
        ordering="specialite",
        description="Rôle",
    )
    def spec(self, obj):
        return obj.specialite 
    
    @admin.display(
        ordering="actif",
        description="Actif ?",
    )
    def status(self, obj):
        if obj.actif == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# Les liens sociale des chefs
@admin.register(Liensociale)
class liensocialeAdmin(ModelAdmin):
    list_display = ('designation', 'lien', 'chef')  
    search_fields = ('designation',)             # rechercher par designation  
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  
    list_filter = [  
        ("id_chef", RelatedDropdownFilter), 
    ]
    
    @admin.display(
        ordering="id_chef",
        description="Chefs",
    )
    def chef(self, obj):
        return obj.id_chef 


# Pour afficher les plats des menus en tab inline
class platInline(StackedInline):
    model = Plat
    extra = 3
    tab = True  


# Les menus
@admin.register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ('nom', 'status', 'pinned', 'create_date')  
    search_fields = ('nom',)             # Permet de rechercher par nom  
    
    inlines = [platInline] # Possiblité d'ajouter en même temps les plats du menu
    
    #list_filter_submit = True  # Bouton de soumission en bas du filtre
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    """
    list_filter = [
        Chef_Fullname_DropdownFilter, 
        ("date_creation", RangeDateFilter),
    ]  
    """  
    @admin.display(
        ordering="actif",
        description="Visible ?",
    )
    def status(self, obj):
        if obj.actif == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="pinned",
        description="Épingler ?",
    )
    def pinned(self, obj):
        if obj.pinned == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# Les plats des menus
@admin.register(Plat)
class platAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    
    list_display = ('nom', 'status', 'pinned', 'menu', 'create_date')  
    search_fields = ('designation',)             # rechercher par designation  
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  
    list_filter = [  
        ("id_menu", RelatedDropdownFilter),
        ("date_creation", RangeDateFilter),
    ]
    
    @admin.display(
        ordering="actif",
        description="Visible ?",
    )
    def status(self, obj):
        if obj.actif == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="pinned",
        description="Épingler ?",
    )
    def pinned(self, obj):
        if obj.pinned == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="id_menu",
        description="Menu",
    )
    def menu(self, obj):
        return obj.id_menu
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


"""
class Serviceclient_TextFilter(TextFilter):
    title = _("Custom filter")
    parameter_name = "nom"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            # Here write custom query
            return queryset.filter(your_field=self.value())

        return queryset
"""


# Les agents du service clients
@admin.register(Service_client)
class ServiceclientAdmin(ModelAdmin):
    list_display = ('nom', 'email', 'status', 'create_date')  
    search_fields = ('nom', 'email',)             # Permet de rechercher par nom ou email 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("nom", FieldTextFilter),
        ("date_creation", RangeDateFilter),
    ]  
    
    
    @admin.display(
        ordering="actif",
        description="Actif ?",
    )
    def status(self, obj):
        if obj.actif == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# newsletter_email pour stocker les emails des visiteurs pour les articles
@admin.register(Newsletter_email)
class NewsletteremailAdmin(ModelAdmin):
    list_display = ('mail', 'status')  
    search_fields = ('email_visteur',)             # Permet de rechercher par email 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("email_visteur", FieldTextFilter), 
    ]  
    
    @admin.display(
        ordering="actif",
        description="Actif ?",
    )
    def status(self, obj):
        if obj.actif == True :
            return "OUI"
        else:
            return "NON" 
    
    @admin.display(
        ordering="email_visteur",
        description="Email",
    )
    def mail(self, obj):
        return obj.email_visteur


# newsletter_email pour stocker les emails des visiteurs pour les articles
@admin.register(Contact_company)
class Contact_companyAdmin(ModelAdmin):
    list_display = ('contact', 'create_date')  
    search_fields = ('contact',)             # Permet de rechercher par contact 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("contact", FieldTextFilter), 
    ]   
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# liensociale_company pour stocker les lien sociales du restaurant
@admin.register(Liensociale_company)
class Liensociale_companyAdmin(ModelAdmin):
    list_display = ('designation', 'lien')  
    search_fields = ('designation',)             # Permet de rechercher par designation 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("designation", FieldTextFilter), 
    ]   


# email_send pour stocker les emails des visiteurs et en même temps envoyer aux agents du service clients
@admin.register(Email_send)
class Email_sendAdmin(ModelAdmin):
    list_display = ('nom', 'email', 'create_date')  
    search_fields = ('nom',)             # Permet de rechercher par contact 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("nom", FieldTextFilter), 
    ]   
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# studio_info pour stocker les infos du restaurant
@admin.register(Studio_info)
class Studio_infoAdmin(ModelAdmin):
    list_display = ('name', 'adresse', 'Email', 'create_date')  
    search_fields = ('app_name',)             # Permet de rechercher par app_name 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("app_name", FieldTextFilter), 
    ]   
    
    
    @admin.display(
        ordering="app_name",
        description="Nom",
    )
    def name(self, obj):
        return obj.app_name
    
    
    @admin.display(
        ordering="app_adresse",
        description="adresse",
    )
    def adresse(self, obj):
        return obj.app_adresse
    
    
    @admin.display(
        ordering="app_mailadresse",
        description="Email",
    )
    def Email(self, obj):
        return obj.app_mailadresse
    
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


# article pour stocker les articles du blog du restaurant
@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
    
    list_display = ('titre', 'publish', 'create_date')  
    prepopulated_fields = {"slug": ("titre",)} # mis à jour automatiquement lorsque nous définissons le titre
    search_fields = ('titre',)             # Permet de rechercher par contact 
    
    # ajout de filtrage à l’aide de l’attribut list_filter
    list_filter_submit = True  # Bouton de soumission en bas du filtre
    list_filter = [
        ("titre", FieldTextFilter), 
    ]     
    
    @admin.display(
        ordering="status",
        description="Publier ?",
    )
    def publish(self, obj):
        if obj.status == True:
            return "OUI"
        else:
            return "NON"
    
    
    @admin.display(
        ordering="date_creation",
        description="Date Ajout",
    )
    def create_date(self, obj):
        return obj.date_creation


