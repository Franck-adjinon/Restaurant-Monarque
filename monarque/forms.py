from django import forms 


# Formulaire pour l'envoie de message
class MessageForm(forms.Form):
    nom = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "common-input mt-10", "placeholder": "Nom & Prénom"}
        ),
    )
    email = forms.EmailField( 
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "common-input mt-10", "placeholder": "Email"}
        ),
    )
    sujet = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "common-input mt-10", "placeholder": "Sujet"}
        ),
    )
    message = forms.CharField( 
        required=True,
        max_length=255,
        widget=forms.Textarea(
            attrs={
                "class": "common-textarea mt-10",
                "rows": 7,
                "cols": 30,
                "placeholder": "Message",
            }
        ),
    )
