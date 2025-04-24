# Règles de versionnage

## Conventions de commit
- Format : `<type>(<scope>): <description>`
- Types autorisés : `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
## Détails :
type : Indique la nature du changement. Voici quelques types courants :
-feat : Pour une nouvelle fonctionnalité.
-fix : Pour une correction de bug.
-docs : Pour des changements dans la documentation.
-style : Pour des modifications qui n’affectent pas la logique (ex. formatage, indentation).
-refactor : Pour une restructuration ou amélioration du code existant sans ajout de fonctionnalité.
-test : Pour l'ajout ou la modification de tests.
-chore : Pour les tâches de maintenance (ex. mise à jour des dépendances).
# scope : La partie du projet concernée (optionnel mais recommandé).

Exemples : etudiant, rapport, CSS, admin.
# description : Une brève description des changements effectués.
Soyez précis et utilisez un ton impératif : "ajout," "modifie," "supprime," etc.

## Exemples 
  - `feat(soutenance): ajout du modèle pour la table soutenance`
  - `fix(css): correction du style des boutons`

## Conventions de branches
- Branche principale : `main`
- Branche de développement : `develop`
- Format des branches fonctionnelles : `<type>/<description-courte>`
  - Exemples : `feat/ajout-page-admin`, `fix/bug-css-affichage`.


