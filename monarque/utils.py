# TODO: Fonctions de rappel d'environnement
def environment_callback(request):
    """
    Permet d'indiquer aux administrateurs dans quel environnement ils travaillent (ex. : Production, Développement, etc.)
    """
    return ["Developpement", "info"] # info, danger, warning, success