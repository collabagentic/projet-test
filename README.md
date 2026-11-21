# projet-test

Projet d'essai pour valider la chaîne de l'agence : développement, tests, revue sécurité, pull request.

## Utilisation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

## Contenu

- `hello.py` : fonctions `greet(name)` (bonjour) et `farewell(name)` (au revoir). Les deux retirent les espaces autour du nom et lèvent `ValueError` si le nom est vide.
- `tests/` : tests `pytest`.
- `.github/workflows/ci.yml` : lint (ruff), analyse de sécurité (bandit) et tests à chaque pull request.

## Règles

- Aucun secret dans le dépôt (voir `.gitignore`). Les clés passent par des variables d'environnement.
- Le développement se fait sur une branche dédiée, jamais directement sur `main`.
- Toute fusion dans `main` passe par une pull request approuvée par un humain.

## Cockpit de l'élève — mission M-005 (contenant)

Contenant (moteur) uniquement ; aucun contenu de domaine (mineurs/santé) n'est
codé en dur.

- `cockpit/` : moteur de questionnaire, génération de site standalone, rendu
  de roadmap et filtre de termes interdits.
- `config/` : configuration chargée au runtime (emplacements `A_DEFINIR_<SUJET>`).
- `tests/` : tests `pytest` (fixtures marquées `FICTIF`, environnement non exposé).

Démonstration (données FICTIF, sortie non exposée) :

```bash
python -m cockpit
```

Vérifications :

```bash
pytest
ruff check .
bandit -q -r . -x ./tests,./.venv
```
