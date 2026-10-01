# 🎓 GUIDE COMPLET DU PROJET - Pour Débutants

## 📚 Table des Matières

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Semaine 1 - Fichiers et Explications](#semaine-1---préparation-base-de-connaissances)
3. [Semaine 2 - Fichiers et Explications](#semaine-2---chaîne-langchain-basique)
4. [Fichiers de Configuration](#fichiers-de-configuration)
5. [Fichiers de Test](#fichiers-de-test)
6. [Comment Tout Fonctionne Ensemble](#comment-tout-fonctionne-ensemble)
7. [Comment Utiliser le Projet](#comment-utiliser-le-projet)

---

## 🎯 Vue d'ensemble du projet

### Qu'est-ce que ce projet fait ?

Ce projet est une **IA qui recommande des templates de sites web** pour SidiWeb. Quand un utilisateur dit "Je veux un site pour ma startup moderne", l'IA:

1. Analyse la demande
2. Trouve les meilleurs templates
3. Recommande des couleurs appropriées
4. Suggère des polices de caractères

### Technologies utilisées

- **Python 3.11+** : Langage de programmation
- **LangChain** : Framework pour construire des applications avec des LLM (Large Language Models)
- **OpenAI GPT-3.5-turbo** : L'intelligence artificielle qui comprend et génère les recommandations
- **Pydantic** : Pour valider que les données sont correctes

---

## 📁 Semaine 1 - Préparation Base de Connaissances

**Objectif :** Préparer toutes les données dont l'IA a besoin pour faire des recommandations.

### 📂 Structure des dossiers Week 1

```
data/
├── backend_templates/          ← Templates JSON du backend
│   ├── template_service.json
│   ├── template_vitrine.json
│   ├── template_startup.json
│   ├── ... (11 templates au total)
│   └── embeddings/             ← Versions texte pour l'IA
│       ├── service_professionnel.txt
│       ├── site_vitrine.txt
│       └── ... (11 fichiers texte)
├── design_notes/
│   └── analysis.md             ← Notes sur les choix de design
└── design_system.json          ← FICHIER PRINCIPAL (source unique)
```

---

### 📄 Fichier 1 : `data/backend_templates/*.json` (11 fichiers)

**Rôle :** Contiennent les **vrais templates** créés par l'équipe backend.

**Contenu d'un template (exemple `template_service.json`):**

```json
{
  "id": "service_professionnel",
  "name": "Site Service Professionnel",
  "description": "Template pour entreprises de services (conseil, agence, etc.)",
  "category": "service",
  "layout": "Service professionnel",
  "pages": [
    "Accueil",
    "Services",
    "À propos",
    "Portfolio/Réalisations",
    "Témoignages",
    "Contact"
  ],
  "features": [
    "Présentation des services",
    "Grille de services avec icônes",
    "Section portfolio/projets",
    "Formulaire de contact avancé",
    "Section témoignages clients",
    "Call-to-action pour demande de devis"
  ],
  "colors": {
    "primary": "#2C5282",
    "secondary": "#4299E1",
    "accent": "#F6AD55",
    "background": "#F7FAFC",
    "text": "#2D3748"
  }
}
```

**Explication pour débutant :**

- **id** : Nom technique unique (comme un numéro de carte d'identité)
- **name** : Nom lisible par les humains
- **description** : À quoi sert ce template
- **category** : Type de site (service, startup, vitrine, etc.)
- **layout** : Type de mise en page
- **pages** : Quelles pages sont incluses
- **features** : Quelles fonctionnalités le template offre
- **colors** : Palette de 5 couleurs avec codes HEX (ex: #2C5282 = bleu foncé)

**Pourquoi c'est important :** Ces fichiers sont la **base de données** de tous les templates disponibles. L'IA utilise ces informations pour savoir quoi recommander.

---

### 📄 Fichier 2 : `data/design_system.json` ⭐ **LE PLUS IMPORTANT**

**Rôle :** C'est la **source unique de vérité** (single source of truth). Tout le système lit ce fichier.

**Structure complète :**

```json
{
  "templates": [
    {
      "id": "service_professionnel",
      "category": "service",
      "layout": "Service professionnel",
      "description": "Template pour entreprises de services",
      "pages": ["Accueil", "Services", "À propos", ...],
      "features": ["Présentation des services", ...],
      "colors": {
        "primary": "#2C5282",
        "secondary": "#4299E1",
        "accent": "#F6AD55",
        "background": "#F7FAFC",
        "text": "#2D3748"
      },
      "style_tags": ["professionnel", "corporate", "moderne"]
    }
    // ... 10 autres templates
  ],

  "color_palettes": [
    {
      "id": "palette_service_pro",
      "name": "Service Professionnel",
      "primary": "#2C5282",
      "secondary": "#4299E1",
      "accent": "#F6AD55",
      "background": "#F7FAFC",
      "text": "#2D3748",
      "associated_templates": ["service_professionnel"]
    }
    // ... 10 autres palettes
  ],

  "font_pairings": [
    {
      "id": "pairing_moderne",
      "name": "Moderne Professionnel",
      "heading": "Inter",
      "body": "Open Sans",
      "style": "moderne",
      "layouts": ["Service professionnel", "Startup dynamique", "Landing page"]
    }
    // ... 7 autres paires de polices
  ],

  "style_mappings": {
    "moderne": ["service_professionnel", "startup_tech", ...],
    "professionnel": ["service_professionnel", "entreprise_classique", ...],
    "simple": ["site_vitrine", "cv_en_ligne", ...],
    // ... autres styles
  }
}
```

**Explication détaillée pour débutant :**

#### Section `templates` :

- Contient **11 templates** complets
- Chaque template a :
  - **id** : Identifiant unique
  - **category** : Type de site (service, startup, landing, etc.)
  - **layout** : Type de mise en page visuelle
  - **description** : Ce que fait ce template
  - **pages** : Liste des pages incluses
  - **features** : Liste des fonctionnalités
  - **colors** : 5 couleurs (primary, secondary, accent, background, text)
  - **style_tags** : Mots-clés de style (ex: ["moderne", "professionnel"])

#### Section `color_palettes` :

- **11 palettes** de couleurs (une par template)
- Chaque palette contient :
  - **id** : Identifiant de la palette
  - **name** : Nom descriptif
  - **primary** : Couleur principale (ex: #2C5282 = bleu foncé)
  - **secondary** : Couleur secondaire
  - **accent** : Couleur d'accent (pour boutons, highlights)
  - **background** : Couleur de fond
  - **text** : Couleur du texte
  - **associated_templates** : Quels templates utilisent cette palette

**Analogie :** C'est comme une boîte de peinture avec des couleurs qui vont bien ensemble.

#### Section `font_pairings` :

- **8 paires de polices** (fonts)
- Chaque paire contient :
  - **heading** : Police pour les titres (ex: "Inter")
  - **body** : Police pour le texte normal (ex: "Open Sans")
  - **style** : Style associé (ex: "moderne")
  - **layouts** : Quels layouts utilisent cette paire

**Analogie :** C'est comme choisir une police élégante pour les titres et une police lisible pour le texte.

#### Section `style_mappings` :

- Associe chaque **style** (moderne, professionnel, etc.) à une **liste de templates**
- Permet de trouver rapidement : "Quels templates sont 'modernes' ?"

**Pourquoi c'est important :** Ce fichier est lu par le code Python pour savoir quels templates, couleurs et polices recommander. Si vous modifiez ce fichier, tout le système est mis à jour automatiquement.

---

### 📄 Fichiers 3 : `data/backend_templates/embeddings/*.txt` (11 fichiers)

**Rôle :** Versions **texte enrichies** des templates pour la recherche sémantique (recherche par sens, pas par mots exacts).

**Exemple de contenu (`service_professionnel.txt`):**

```markdown
# Template: Service Professionnel

**ID:** service_professionnel
**Catégorie:** Service
**Layout:** Service professionnel

## Description

Template moderne et professionnel spécialement conçu pour les entreprises
de services telles que les agences de conseil, cabinets d'expertise,
sociétés de services B2B, etc. Met en valeur l'expertise et la crédibilité
avec un design corporate et rassurant.

## Pages incluses

- Accueil : Vue d'ensemble des services
- Services : Détail de chaque offre
- À propos : Histoire et équipe
- Portfolio/Réalisations : Projets clients
- Témoignages : Avis clients
- Contact : Formulaire et coordonnées

## Fonctionnalités

- Présentation claire des services avec grille organisée
- Icônes professionnelles pour chaque service
- Section portfolio avec filtres par type de projet
- Formulaire de contact avancé avec sélection de service
- Carrousel de témoignages clients
- Call-to-action pour demande de devis rapide

## Style visuel

Design corporate avec palette bleue professionnelle. Crée une atmosphère
de confiance et d'expertise, idéale pour les services B2B et conseils
professionnels.

## Couleurs

- **Primary (#2C5282)** : Bleu foncé professionnel - confiance et stabilité
- **Secondary (#4299E1)** : Bleu clair moderne - accessibilité et innovation
- **Accent (#F6AD55)** : Orange chaleureux - appel à l'action et dynamisme
- **Background (#F7FAFC)** : Gris très clair - clarté et propreté
- **Text (#2D3748)** : Gris foncé - lisibilité optimale

## Typographie recommandée

- **Titres :** Inter (moderne, géométrique, professionnel)
- **Corps :** Open Sans (lisible, neutre, polyvalent)

## Cas d'usage idéaux

- Agences de conseil en management
- Cabinets d'expertise comptable
- Sociétés de services informatiques
- Agences de marketing et communication
- Cabinets juridiques modernes
- Services de formation professionnelle
- Sociétés de consulting RH
- Agences de design et création
- Services aux entreprises B2B
- Bureaux d'études techniques

## Mots-clés

service, professionnel, conseil, agence, expertise, B2B, corporate,
crédibilité, témoignages, portfolio, réalisations, devis, contact,
confiance, moderne, bleu, orange, clean, organisé, grille, icônes,
formulaire, clients, projets, équipe, about, services multiples
```

**Explication pour débutant :**

Imaginez que vous demandez à l'IA : "Je veux un site pour mon agence de conseil".

- **Avec seulement le JSON** : L'IA cherche le mot "conseil" dans les fichiers. Si le mot exact n'existe pas, elle ne trouve rien.
- **Avec le fichier texte** : L'IA comprend que "agence de conseil" est similaire à "services professionnels", "expertise", "consulting", etc. Elle trouve le bon template même si vous n'utilisez pas les mots exacts !

**Pourquoi c'est important :** Ces fichiers permettent une **recherche intelligente** (sémantique). L'IA comprend le **sens** de votre demande, pas juste les mots.

**Usage futur :** Avec LangChain et OpenAI Embeddings, on peut créer une base de données vectorielle pour trouver automatiquement les templates les plus pertinents.

---

### 📄 Fichier 4 : `data/design_notes/analysis.md`

**Rôle :** Documentation des **décisions de design** prises lors de la création du système.

**Contenu :**

- Explication de pourquoi certaines couleurs ont été choisies
- Logique derrière les associations polices-layouts
- Notes sur les style_tags de chaque template

**Explication pour débutant :** C'est comme un journal de bord qui explique **pourquoi** les choses ont été faites d'une certaine manière. Utile pour comprendre les choix.

**Pourquoi c'est important :** Quand quelqu'un se demande "Pourquoi le template startup utilise ces couleurs ?", la réponse est dans ce fichier.

---

### 📄 Fichier 5 : `prompts/variables.py`

**Rôle :** Définit les **variables d'entrée** que l'utilisateur peut fournir.

**Contenu complet :**

```python
"""
Variables pour le prompt de recommandation de design
"""

# Variables principales
DESIGN_PROMPT_VARIABLES = {
    "category": "Catégorie du site web (service, vitrine, startup, landing, etc.)",
    "style": "Style visuel souhaité (moderne, professionnel, simple, classique, etc.)",
    "preferences": "Préférences spécifiques de l'utilisateur (couleurs, fonctionnalités, etc.)"
}

# Valeurs valides pour category
VALID_CATEGORIES = [
    "service",      # Services professionnels (conseil, agence, etc.)
    "vitrine",      # Site vitrine classique
    "startup",      # Startup tech/innovante
    "landing",      # Landing page
    "freelance",    # Portfolio freelance
    "evenement",    # Site d'événement
    "entreprise",   # Site d'entreprise classique
    "education",    # Plateforme éducative
    "cv",           # CV en ligne
    "association",  # Site d'association
    "artisan"       # Site d'artisan local
]

# Valeurs valides pour style
VALID_STYLES = [
    "moderne",       # Design contemporain, épuré
    "professionnel", # Corporate, sérieux
    "simple",        # Minimaliste, clair
    "classique",     # Traditionnel, élégant
    "minimal",       # Ultra-épuré
    "dynamique",     # Énergique, coloré
    "corporate",     # Formel, entreprise
    "academique"     # Éducatif, structuré
]

# Champs requis
REQUIRED_FIELDS = ["category", "style"]

# Suggestions de styles par catégorie
CATEGORY_STYLE_SUGGESTIONS = {
    "service": ["professionnel", "moderne", "corporate"],
    "vitrine": ["simple", "classique", "moderne"],
    "startup": ["moderne", "dynamique"],
    "landing": ["dynamique", "moderne", "minimal"],
    "freelance": ["moderne", "minimal", "dynamique"],
    "evenement": ["dynamique", "moderne"],
    "entreprise": ["corporate", "professionnel", "classique"],
    "education": ["academique", "professionnel", "simple"],
    "cv": ["minimal", "moderne", "professionnel"],
    "association": ["simple", "classique"],
    "artisan": ["simple", "classique"]
}
```

**Explication pour débutant :**

Ce fichier documente :

- **category** : Le type de site que l'utilisateur veut (11 options)
- **style** : Le style visuel souhaité (8 options)
- **preferences** : Détails supplémentaires (texte libre)

**Exemple d'utilisation :**

```python
# L'utilisateur veut :
category = "startup"
style = "moderne"
preferences = "Je veux des couleurs vives et un design audacieux"
```

**Pourquoi c'est important :** Définit clairement ce que l'utilisateur peut demander. C'est la "fiche de commande" du système.

---

### 📄 Fichier 6 : `prompts/initial_prompt.txt`

**Rôle :** Les **instructions données à l'IA** (GPT-3.5-turbo). C'est comme le manuel d'utilisation pour l'IA.

**Contenu complet :**

```
Tu es un expert en design web et recommandation de templates.

USER INPUT VARIABLES:
- category: La catégorie du site web demandée (service, vitrine, startup, landing, freelance, evenement, entreprise, education, cv, association, artisan)
- style: Le style visuel souhaité (moderne, professionnel, simple, classique, minimal, dynamique, corporate, academique)
- preferences: Les préférences spécifiques de l'utilisateur

DESIGN SYSTEM AVAILABLE:
Tu as accès à un design_system.json contenant :
- templates : Liste de 11 templates avec leurs caractéristiques
- color_palettes : 11 palettes de couleurs
- font_pairings : 8 paires de polices
- style_mappings : Associations entre styles et templates

MATCHING LOGIC:
1. Templates : Trouve les templates qui correspondent à la category d'abord
2. Style : Filtre par style_tags qui matchent avec le style demandé
3. Preferences : Ajuste selon les préférences spécifiques

RECOMMENDATION OUTPUT:
Tu dois retourner UNIQUEMENT un objet JSON valide avec cette structure exacte:

{
  "templates": ["template_id_1", "template_id_2", "template_id_3"],
  "colors": {
    "primary": "#HEX",
    "secondary": "#HEX",
    "accent": "#HEX",
    "background": "#HEX",
    "text": "#HEX"
  },
  "fonts": {
    "heading": "NomDeLaPolice",
    "body": "NomDeLaPolice"
  },
  "explanation": "Explication courte de pourquoi ces choix"
}

RULES:
- Toujours recommander 3 templates (maximum)
- Les template IDs doivent exister dans le design_system
- Les couleurs doivent être au format HEX (#RRGGBB)
- L'explication doit être concise (2-3 phrases)
- Retourner UNIQUEMENT le JSON, aucun texte avant ou après
```

**Explication pour débutant :**

Ce fichier dit à l'IA :

1. **Qui tu es** : "Tu es un expert en design web"
2. **Quelles données tu as** : "Tu as accès à design_system.json"
3. **Comment faire le matching** :
   - D'abord, cherche par catégorie
   - Ensuite, filtre par style
   - Affine avec les préférences
4. **Quel format de réponse** : "Retourne un JSON avec templates, colors, fonts, explanation"

**Analogie :** C'est comme donner une fiche de poste à un employé. L'IA sait exactement quoi faire et comment le faire.

**Pourquoi c'est important :** Sans ce prompt, l'IA ne saurait pas comment analyser les demandes ou quel format de réponse donner.

---

## 🔗 Semaine 2 - Chaîne LangChain Basique

**Objectif :** Créer le **code Python** qui utilise LangChain et GPT-3.5-turbo pour générer des recommandations.

### 📂 Structure des dossiers Week 2

```
src/
├── models/
│   ├── __init__.py
│   └── output_models.py        ← Modèles Pydantic
├── chains/
│   ├── __init__.py
│   └── recommendation_chain.py ← CODE PRINCIPAL
├── test_recommendation_chain.py
├── manual_test.py
└── simple_test.py
```

---

### 📄 Fichier 7 : `src/models/output_models.py` ⭐

**Rôle :** Définit les **modèles Pydantic** qui valident la structure de la réponse de l'IA.

**Contenu complet :**

```python
from pydantic import BaseModel, Field
from typing import List, Dict

class RecommendationOutput(BaseModel):
    """
    Modèle simple pour la sortie de la chaîne de recommandation.

    Attributs:
        templates: Liste des IDs de templates recommandés
        colors: Liste des codes couleur HEX recommandés
        fonts: Dictionnaire avec les polices pour heading et body
    """
    templates: List[str] = Field(description="Liste des IDs de templates recommandés")
    colors: List[str] = Field(description="Liste des codes couleur HEX")
    fonts: Dict[str, str] = Field(description="Polices pour heading et body")


class DetailedRecommendationOutput(BaseModel):
    """
    Modèle détaillé pour la sortie de la chaîne de recommandation.

    Attributs:
        templates: Liste des IDs de templates recommandés
        colors: Dictionnaire avec primary, secondary, accent, background, text
        fonts: Dictionnaire avec les polices pour heading et body
        explanation: Explication de pourquoi ces recommandations
    """
    templates: List[str] = Field(
        description="Liste des IDs de templates recommandés (max 3)"
    )
    colors: Dict[str, str] = Field(
        description="Palette de couleurs avec primary, secondary, accent, background, text en HEX"
    )
    fonts: Dict[str, str] = Field(
        description="Polices recommandées avec heading et body"
    )
    explanation: str = Field(
        description="Explication courte de pourquoi ces recommandations"
    )
```

**Explication pour débutant :**

**Pydantic** est une bibliothèque Python qui :

- **Valide** que les données sont correctes
- **Documente** la structure attendue
- **Empêche les erreurs** en vérifiant automatiquement

**Deux modèles :**

1. **RecommendationOutput** (simple) :
   - `templates` : Liste de strings (ex: ["startup_tech", "service_professionnel"])
   - `colors` : Liste de strings (ex: ["#2C5282", "#4299E1"])
   - `fonts` : Dictionnaire (ex: {"heading": "Inter", "body": "Open Sans"})

2. **DetailedRecommendationOutput** (détaillé) :
   - `templates` : Liste de strings (max 3)
   - `colors` : Dictionnaire complet (ex: {"primary": "#2C5282", "secondary": "#4299E1", ...})
   - `fonts` : Dictionnaire (heading/body)
   - `explanation` : String expliquant les choix

**Analogie :** C'est comme un formulaire avec des cases à remplir. Pydantic vérifie que toutes les cases sont remplies correctement.

**Pourquoi c'est important :**

- Garantit que l'IA retourne toujours le bon format
- Si l'IA fait une erreur, Pydantic la détecte immédiatement
- Rend le code plus sûr et plus facile à maintenir

---

### 📄 Fichier 8 : `src/chains/recommendation_chain.py` ⭐⭐⭐ **LE PLUS IMPORTANT**

**Rôle :** C'est le **cœur du système**. Créé la chaîne LangChain qui génère les recommandations.

**Contenu complet avec explications :**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pathlib import Path
import json
import os

from src.models.output_models import DetailedRecommendationOutput


class RecommendationChain:
    """
    Chaîne LangChain pour générer des recommandations de design web.

    Cette classe encapsule toute la logique de recommandation :
    1. Charge le design system
    2. Crée le prompt template
    3. Configure le LLM (GPT-3.5-turbo)
    4. Parse la sortie JSON
    5. Génère les recommandations
    """

    def __init__(self):
        """Initialise la chaîne de recommandation."""
        # Charger le design system depuis le fichier JSON
        self.design_system = self._load_design_system()

        # Créer le prompt template avec les instructions
        self.prompt = self._create_prompt_template()

        # Configurer le LLM (GPT-3.5-turbo)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,  # Créativité modérée
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Configurer le parser JSON avec validation Pydantic
        self.parser = JsonOutputParser(pydantic_object=DetailedRecommendationOutput)

        # Construire la chaîne complète
        self.chain = self._build_chain()

    def _load_design_system(self) -> dict:
        """
        Charge le fichier design_system.json.

        Returns:
            dict: Le contenu du design system
        """
        # Trouver le chemin du fichier (fonctionne peu importe où on exécute)
        project_root = Path(__file__).parent.parent.parent
        design_system_path = project_root / "data" / "design_system.json"

        with open(design_system_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """
        Crée le template de prompt avec les instructions pour l'IA.

        Returns:
            ChatPromptTemplate: Le prompt configuré
        """
        # Charger les instructions depuis le fichier
        project_root = Path(__file__).parent.parent.parent
        prompt_path = project_root / "prompts" / "initial_prompt.txt"

        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_message = f.read()

        # Créer le template avec variables category, style, preferences
        template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", """
            Je souhaite créer un site web avec les caractéristiques suivantes:

            Catégorie: {category}
            Style: {style}
            Préférences: {preferences}

            Design System disponible:
            {design_system}

            Recommande-moi les meilleurs templates, couleurs et polices.
            """)
        ])

        return template

    def _build_chain(self):
        """
        Construit la chaîne LangChain complète.

        La chaîne suit ce flux:
        Prompt → LLM → Parser JSON → Output validé

        Returns:
            La chaîne LangChain configurée
        """
        return self.prompt | self.llm | self.parser

    def invoke(self, category: str, style: str, preferences: str = "") -> dict:
        """
        Génère une recommandation basée sur les inputs utilisateur.

        Args:
            category: La catégorie du site (service, startup, etc.)
            style: Le style visuel (moderne, professionnel, etc.)
            preferences: Préférences additionnelles (optionnel)

        Returns:
            dict: Les recommandations avec templates, colors, fonts, explanation

        Example:
            >>> chain = RecommendationChain()
            >>> result = chain.invoke(
            ...     category="startup",
            ...     style="moderne",
            ...     preferences="Couleurs vives et audacieuses"
            ... )
            >>> print(result['templates'])
            ['startup_tech', 'landing_page']
        """
        # Convertir le design system en JSON string
        design_system_json = json.dumps(self.design_system, indent=2, ensure_ascii=False)

        # Invoquer la chaîne avec les paramètres
        result = self.chain.invoke({
            "category": category,
            "style": style,
            "preferences": preferences,
            "design_system": design_system_json
        })

        return result
```

**Explication ligne par ligne pour débutant :**

#### Imports :

```python
from langchain_core.prompts import ChatPromptTemplate
```

- **ChatPromptTemplate** : Pour créer le message envoyé à l'IA

```python
from langchain_openai import ChatOpenAI
```

- **ChatOpenAI** : Pour se connecter à GPT-3.5-turbo

```python
from langchain_core.output_parsers import JsonOutputParser
```

- **JsonOutputParser** : Pour convertir la réponse texte de l'IA en JSON Python

#### Classe RecommendationChain :

**Méthode `__init__`** (constructeur) :

```python
def __init__(self):
    self.design_system = self._load_design_system()  # Charge design_system.json
    self.prompt = self._create_prompt_template()     # Charge initial_prompt.txt
    self.llm = ChatOpenAI(...)                       # Configure GPT-3.5-turbo
    self.parser = JsonOutputParser(...)              # Configure validation Pydantic
    self.chain = self._build_chain()                 # Crée la chaîne complète
```

**Analogie :** C'est comme préparer tous les ingrédients avant de cuisiner.

**Méthode `_load_design_system`** :

```python
def _load_design_system(self) -> dict:
    # Trouve le fichier design_system.json
    project_root = Path(__file__).parent.parent.parent
    design_system_path = project_root / "data" / "design_system.json"

    # Ouvre et lit le fichier
    with open(design_system_path, 'r', encoding='utf-8') as f:
        return json.load(f)
```

**Explication :** Ouvre le fichier JSON et le convertit en dictionnaire Python.

**Méthode `_create_prompt_template`** :

```python
def _create_prompt_template(self) -> ChatPromptTemplate:
    # Charge initial_prompt.txt
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_message = f.read()

    # Crée un template avec des variables {category}, {style}, etc.
    template = ChatPromptTemplate.from_messages([
        ("system", system_message),  # Instructions pour l'IA
        ("human", "Je veux un site {category} de style {style}...")  # Message utilisateur
    ])

    return template
```

**Explication :** Crée un "modèle de conversation" avec des trous à remplir (variables).

**Méthode `_build_chain`** :

```python
def _build_chain(self):
    return self.prompt | self.llm | self.parser
```

**Explication :** L'opérateur `|` (pipe) crée une chaîne :

1. **prompt** : Prépare le message
2. **llm** : Envoie à GPT-3.5-turbo
3. **parser** : Convertit la réponse en JSON

**Analogie :** C'est comme une chaîne de production : matières premières → transformation → produit final.

**Méthode `invoke`** (la plus utilisée) :

```python
def invoke(self, category: str, style: str, preferences: str = "") -> dict:
    # Prépare le design system en JSON
    design_system_json = json.dumps(self.design_system, indent=2, ensure_ascii=False)

    # Exécute la chaîne avec les paramètres
    result = self.chain.invoke({
        "category": category,
        "style": style,
        "preferences": preferences,
        "design_system": design_system_json
    })

    return result
```

**Explication :**

1. Convertit `design_system` (dict Python) en string JSON
2. Appelle la chaîne avec les paramètres utilisateur
3. Retourne le résultat (dict Python validé par Pydantic)

**Exemple d'utilisation :**

```python
chain = RecommendationChain()
result = chain.invoke(
    category="startup",
    style="moderne",
    preferences="Je veux des couleurs vives"
)

print(result)
# {
#   "templates": ["startup_tech", "landing_page"],
#   "colors": {"primary": "#FF6B35", "secondary": "#004E89", ...},
#   "fonts": {"heading": "Montserrat", "body": "Roboto"},
#   "explanation": "Ces templates correspondent à une startup moderne avec..."
# }
```

**Pourquoi c'est important :** C'est le fichier qui fait **tout le travail**. Sans lui, rien ne fonctionne.

---

## ⚙️ Fichiers de Configuration

### 📄 Fichier 9 : `requirements.txt`

**Rôle :** Liste toutes les **bibliothèques Python** nécessaires au projet.

**Contenu :**

```
langchain==0.1.0
langchain-openai==0.0.5
langchain-core==0.1.10
pydantic==2.5.3
python-dotenv==1.0.0
openai==1.7.2
```

**Explication pour débutant :**

Chaque ligne est une bibliothèque (package) Python :

- **langchain** : Framework pour applications LLM
- **langchain-openai** : Intégration OpenAI pour LangChain
- **langchain-core** : Composants de base de LangChain
- **pydantic** : Validation de données
- **python-dotenv** : Pour charger les variables d'environnement depuis `.env`
- **openai** : SDK officiel OpenAI

**Comment installer :**

```bash
pip install -r requirements.txt
```

**Analogie :** C'est comme une liste de courses. Vous allez au magasin (PyPI) et achetez tout ce qui est sur la liste.

---

### 📄 Fichier 10 : `.env.example`

**Rôle :** Modèle pour créer votre fichier `.env` avec les clés API.

**Contenu :**

```
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: LangSmith for tracing
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langsmith_api_key_here
```

**Explication pour débutant :**

**Variables d'environnement** = données sensibles qui ne doivent **PAS** être dans le code.

Pour utiliser :

1. Copier `.env.example` → `.env`
2. Remplacer `your_openai_api_key_here` par votre vraie clé API OpenAI
3. Le code lit automatiquement `.env` avec `python-dotenv`

**Pourquoi pas dans le code :**

```python
# ❌ MAUVAIS (clé visible)
api_key = "sk-abc123..."

# ✅ BON (clé dans .env)
api_key = os.getenv("OPENAI_API_KEY")
```

**Pourquoi c'est important :** Protège vos clés API. Si vous partagez le code sur GitHub, votre clé reste secrète.

---

### 📄 Fichier 11 : `.gitignore`

**Rôle :** Dit à Git quels fichiers **ne pas** suivre (ne pas inclure dans le repository).

**Contenu typique :**

```
.env
__pycache__/
*.pyc
.vscode/
venv/
```

**Explication pour débutant :**

- `.env` : Ne pas partager les clés API
- `__pycache__/` : Fichiers Python compilés (auto-générés)
- `*.pyc` : Fichiers bytecode Python (auto-générés)
- `.vscode/` : Paramètres VS Code personnels
- `venv/` : Environnement virtuel Python (trop gros, se régénère)

**Analogie :** C'est comme dire à votre appareil photo de ne pas photographier certaines choses.

---

## 🧪 Fichiers de Test

### 📄 Fichier 12 : `src/test_recommendation_chain.py`

**Rôle :** Tests **complets** avec 5 scénarios différents pour vérifier que tout fonctionne.

**Contenu (résumé):**

```python
def test_service_professionnel():
    """Test pour un site de services professionnels."""
    result = chain.invoke(
        category="service",
        style="professionnel",
        preferences="Site pour une agence de conseil"
    )

    # Vérifications
    assert "templates" in result
    assert "colors" in result
    assert "fonts" in result
    assert len(result["templates"]) <= 3

# ... 4 autres tests (startup, vitrine, cv, landing)
```

**5 scénarios testés :**

1. **Service professionnel** : Agence de conseil
2. **Startup moderne** : Startup tech innovante
3. **Site vitrine** : Petite entreprise
4. **CV en ligne** : Portfolio personnel
5. **Landing page** : Page de lancement produit

**Comment exécuter :**

```bash
pytest src/test_recommendation_chain.py
```

**Explication pour débutant :** Ces tests vérifient automatiquement que le système fonctionne correctement pour différents types de demandes.

---

### 📄 Fichier 13 : `quick_test.py`

**Rôle :** Test **rapide** pour vérifier l'installation et la configuration.

**Contenu :**

```python
from src.chains.recommendation_chain import RecommendationChain
import json

def quick_test():
    """Test rapide de la chaîne de recommandation."""
    print("🚀 Test rapide de la chaîne de recommandation\n")

    # Créer la chaîne
    chain = RecommendationChain()

    # Test simple
    result = chain.invoke(
        category="startup",
        style="moderne",
        preferences="Design audacieux et innovant"
    )

    # Afficher le résultat
    print("✅ Résultat:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    quick_test()
```

**Comment exécuter :**

```bash
python quick_test.py
```

**Explication pour débutant :** C'est le test le plus simple. Si ça marche, tout est bien configuré !

---

### 📄 Fichier 14 : `test_embeddings.py`

**Rôle :** Vérifie que tous les fichiers texte pour embeddings ont été créés correctement.

**Contenu (résumé):**

```python
def test_embeddings():
    """Vérifie que tous les fichiers d'embeddings existent et sont corrects."""

    # Vérifier que le dossier existe
    embeddings_dir = Path("data/backend_templates/embeddings")
    assert embeddings_dir.exists()

    # Vérifier que 11 fichiers .txt existent
    txt_files = list(embeddings_dir.glob("*.txt"))
    assert len(txt_files) == 11

    # Vérifier la structure de chaque fichier
    for file in txt_files:
        content = file.read_text(encoding='utf-8')
        assert "# Template:" in content
        assert "**ID:**" in content
        assert "**Catégorie:**" in content
        # ... autres vérifications

    print("✅ Tous les embeddings sont valides !")
```

**Comment exécuter :**

```bash
python test_embeddings.py
```

**Explication pour débutant :** Vérifie que Week 1 est complète et que tous les fichiers texte ont été créés.

---

## 🔄 Comment Tout Fonctionne Ensemble

### Flux Complet (de A à Z)

```
1. UTILISATEUR fait une demande
   ↓
2. Code Python (recommendation_chain.py) reçoit :
   - category = "startup"
   - style = "moderne"
   - preferences = "Couleurs vives"
   ↓
3. RecommendationChain charge :
   - design_system.json (tous les templates, couleurs, polices)
   - initial_prompt.txt (instructions pour l'IA)
   ↓
4. Création du prompt :
   - Instructions système (initial_prompt.txt)
   - Données utilisateur (category, style, preferences)
   - Design system complet (JSON)
   ↓
5. Envoi à GPT-3.5-turbo via API OpenAI
   ↓
6. GPT-3.5-turbo analyse :
   - Comprend la demande utilisateur
   - Cherche dans le design system
   - Trouve les meilleurs templates
   - Choisit les couleurs appropriées
   - Sélectionne les polices adaptées
   ↓
7. GPT-3.5-turbo retourne JSON :
   {
     "templates": ["startup_tech", "landing_page"],
     "colors": {"primary": "#FF6B35", ...},
     "fonts": {"heading": "Montserrat", "body": "Roboto"},
     "explanation": "Ces templates..."
   }
   ↓
8. JsonOutputParser valide avec Pydantic :
   - Vérifie que tous les champs sont présents
   - Vérifie les types de données
   - Convertit en objet Python
   ↓
9. Résultat retourné à l'utilisateur
   ✅ Recommandations prêtes !
```

### Diagramme Visuel

```
┌─────────────────────────────────────────────────────────────┐
│                         UTILISATEUR                          │
│  "Je veux un site startup moderne avec couleurs vives"      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              src/chains/recommendation_chain.py              │
│                    RecommendationChain                       │
│                                                              │
│  1. Charge design_system.json                               │
│  2. Charge initial_prompt.txt                               │
│  3. Prépare le prompt avec les variables                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    LANGCHAIN PIPELINE                        │
│                                                              │
│  ChatPromptTemplate  →  ChatOpenAI  →  JsonOutputParser    │
│  (Prépare message)      (GPT-3.5)      (Valide JSON)       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA/design_system.json                   │
│                                                              │
│  • 11 templates                                             │
│  • 11 color palettes                                        │
│  • 8 font pairings                                          │
│  • style_mappings                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    OPENAI GPT-3.5-TURBO                      │
│                                                              │
│  Analyse → Matching → Génération de recommandations        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                src/models/output_models.py                   │
│              DetailedRecommendationOutput                    │
│                                                              │
│  Validation Pydantic : templates, colors, fonts, explanation│
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                     RÉSULTAT JSON                            │
│                                                              │
│  {                                                          │
│    "templates": ["startup_tech", "landing_page"],          │
│    "colors": { "primary": "#FF6B35", ... },                │
│    "fonts": { "heading": "Montserrat", "body": "Roboto" }, │
│    "explanation": "Ces templates correspondent..."          │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Comment Utiliser le Projet

### Étape 1 : Installation

```bash
# 1. Cloner le projet (si depuis Git)
git clone <url>
cd sidiweb-workspace

# 2. Créer un environnement virtuel Python
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer la clé API OpenAI
# Copier .env.example → .env
# Éditer .env et ajouter votre clé API
```

### Étape 2 : Test Rapide

```bash
# Test simple pour vérifier que tout fonctionne
python quick_test.py
```

**Résultat attendu :**

```
🚀 Test rapide de la chaîne de recommandation

✅ Résultat:
{
  "templates": [
    "startup_tech",
    "landing_page"
  ],
  "colors": {
    "primary": "#FF6B35",
    "secondary": "#004E89",
    "accent": "#F6AA55",
    "background": "#F9F9F9",
    "text": "#1A1A1A"
  },
  "fonts": {
    "heading": "Montserrat",
    "body": "Roboto"
  },
  "explanation": "Ces templates correspondent parfaitement à une startup moderne..."
}
```

### Étape 3 : Utilisation dans votre Code

```python
from src.chains.recommendation_chain import RecommendationChain

# Créer l'instance
chain = RecommendationChain()

# Faire une recommandation
result = chain.invoke(
    category="service",
    style="professionnel",
    preferences="Site pour une agence de marketing digital"
)

# Utiliser le résultat
print(f"Templates recommandés : {result['templates']}")
print(f"Couleur principale : {result['colors']['primary']}")
print(f"Police des titres : {result['fonts']['heading']}")
print(f"Explication : {result['explanation']}")
```

### Étape 4 : Tests Complets

```bash
# Exécuter tous les tests
pytest src/test_recommendation_chain.py -v

# Vérifier les embeddings
python test_embeddings.py
```

---

## 📚 Résumé des Fichiers par Semaine

### ✅ SEMAINE 1 - Fichiers de Données

| Fichier                                         | Rôle                              | Semaine |
| ----------------------------------------------- | --------------------------------- | ------- |
| `data/backend_templates/*.json` (×11)           | Templates backend originaux       | Week 1  |
| `data/design_system.json`                       | **Source unique de vérité**       | Week 1  |
| `data/backend_templates/embeddings/*.txt` (×11) | Versions texte pour IA            | Week 1  |
| `data/design_notes/analysis.md`                 | Documentation des décisions       | Week 1  |
| `prompts/variables.py`                          | Définition des variables d'entrée | Week 1  |
| `prompts/initial_prompt.txt`                    | Instructions pour GPT             | Week 1  |

### ✅ SEMAINE 2 - Fichiers de Code

| Fichier                              | Rôle                         | Semaine |
| ------------------------------------ | ---------------------------- | ------- |
| `src/models/output_models.py`        | Modèles Pydantic             | Week 2  |
| `src/chains/recommendation_chain.py` | **Code principal LangChain** | Week 2  |
| `src/test_recommendation_chain.py`   | Tests complets (5 scénarios) | Week 2  |
| `src/manual_test.py`                 | Test manuel interactif       | Week 2  |
| `src/simple_test.py`                 | Test simple                  | Week 2  |

### ⚙️ Fichiers de Configuration

| Fichier            | Rôle                       |
| ------------------ | -------------------------- |
| `requirements.txt` | Dépendances Python         |
| `.env.example`     | Modèle pour clés API       |
| `.gitignore`       | Fichiers à ignorer par Git |
| `README.md`        | Documentation principale   |

### 📖 Fichiers de Documentation

| Fichier                     | Rôle                             |
| --------------------------- | -------------------------------- |
| `EMBEDDINGS_COMPLETE.md`    | Guide des embeddings             |
| `GUIDE_WEEK1_COMPLETED.md`  | Résumé Week 1                    |
| `WEEK1_SUMMARY.md`          | Détails Week 1                   |
| `IMPLEMENTATION.md`         | Guide d'implémentation           |
| `UPDATING_DESIGN_SYSTEM.md` | Comment mettre à jour le système |

---

## 🎯 Points Clés pour un Débutant

### Ce que fait le système :

1. **Entrée** : Utilisateur dit ce qu'il veut (catégorie, style, préférences)
2. **Traitement** : IA analyse et cherche dans la base de données
3. **Sortie** : Recommandations (templates, couleurs, polices, explication)

### Les fichiers les plus importants :

1. **data/design_system.json** - Toutes les données
2. **src/chains/recommendation_chain.py** - Tout le code
3. **prompts/initial_prompt.txt** - Instructions pour l'IA

### Comment tester :

```bash
python quick_test.py  # Test le plus simple
```

### Comment utiliser :

```python
from src.chains.recommendation_chain import RecommendationChain

chain = RecommendationChain()
result = chain.invoke(category="startup", style="moderne")
print(result)
```

### En cas de problème :

1. Vérifier que `.env` existe avec votre clé API OpenAI
2. Vérifier que toutes les dépendances sont installées (`pip install -r requirements.txt`)
3. Vérifier que `data/design_system.json` existe
4. Exécuter `python quick_test.py` pour diagnostiquer

---

## 🎓 Prochaines Étapes

### Si vous voulez améliorer :

1. **Ajouter de nouveaux templates** : Modifier `design_system.json`
2. **Améliorer les prompts** : Modifier `initial_prompt.txt`
3. **Ajouter des validations** : Modifier `output_models.py`
4. **Créer une API** : Utiliser FastAPI pour exposer `recommendation_chain.py`

### Pour apprendre plus :

- **LangChain** : https://python.langchain.com/docs/get_started/introduction
- **Pydantic** : https://docs.pydantic.dev/latest/
- **OpenAI API** : https://platform.openai.com/docs/introduction

---

**Date :** 20 février 2026  
**Version :** 1.0  
**Status :** ✅ Week 1 et Week 2 COMPLÈTES

---

## 📞 Questions Fréquentes (FAQ)

**Q: Quel fichier je modifie pour ajouter un nouveau template ?**  
R: `data/design_system.json` - Ajoutez-le dans la section `templates`, puis créez aussi un fichier `.txt` dans `embeddings/`.

**Q: Comment changer les instructions de l'IA ?**  
R: Modifiez `prompts/initial_prompt.txt`.

**Q: Où est stockée ma clé API ?**  
R: Dans le fichier `.env` (à ne JAMAIS partager !).

**Q: Comment exécuter les tests ?**  
R: `python quick_test.py` pour un test simple, ou `pytest src/test_recommendation_chain.py` pour tous les tests.

**Q: Que faire si j'ai l'erreur "OpenAI API key not found" ?**  
R: Créez un fichier `.env` avec `OPENAI_API_KEY=votre_clé`.

**Q: Puis-je utiliser GPT-4 au lieu de GPT-3.5 ?**  
R: Oui ! Dans `recommendation_chain.py`, changez `model="gpt-3.5-turbo"` en `model="gpt-4"`.

---

**Bon apprentissage ! 🚀**
