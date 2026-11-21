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

## Cockpit de l'élève — mission M-004 (P1)

Moteur du parcours P1 (domaine sensible mineurs : on construit le *contenant*, jamais le contenu) :

- cockpit/questionnaire.py : moteur de questionnaire de profil (maximum 15 questions).
- cockpit/filtrage.py : filtre de termes interdits (liste chargée depuis config).
- cockpit/roadmap.py : moteur de roadmap (au moins 3 jalons).
- cockpit/site.py : génération d'un site HTML **standalone** (pas de base centrale, généré en moins de 5 minutes).
- cockpit/pipeline.py : parcours complet questionnaire → profil → site + roadmap.

**Règle de contenu** : aucun contenu de domaine (question, libellé, seuil, recommandation, conseil) n'est écrit en dur. Les textes sont des emplacements A_DEFINIR_<SUJET> chargés depuis config/*.json. La génération est **refusée** tant qu'un emplacement reste ouvert.

Configuration et gabarit :

- config/questionnaire.json
- config/termes_interdits.json
- config/roadmap.json
- config/site.json
- templates/site.html

Vérifications :

    pytest
    ruff check .
    bandit -q -r . -x ./tests,./.venv
