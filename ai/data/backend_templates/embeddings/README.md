# Templates Backend - Format Texte pour Embedding

## 📁 Emplacement

`data/backend_templates/embeddings/`

## 🎯 Objectif

Ces fichiers texte sont des **versions enrichies et descriptives** des templates JSON backend, conçues spécifiquement pour:

1. **Embeddings vectoriels** - Permettre la recherche sémantique
2. **RAG (Retrieval Augmented Generation)** - Enrichir le contexte LLM
3. **Recherche par similarité** - Trouver le template le plus pertinent
4. **Améliorer les recommendations** - Donner plus de contexte à l'AI

## 📄 Format

Chaque fichier `.txt` contient une description complète et structurée:

- **ID et catégorie** - Identification du template
- **Description détaillée** - Contexte complet du template
- **Pages incluses** - Structure du site
- **Fonctionnalités** - Ce que le template peut faire
- **Style visuel** - Description de l'apparence
- **Couleurs** - Palette avec significations
- **Typographie** - Polices recommandées
- **Cas d'usage** - Scénarios d'utilisation
- **Mots-clés** - Pour recherche sémantique

## 🔍 Utilisation

### 1. Avec LangChain Embeddings

```python
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Charger tous les fichiers texte
loader = DirectoryLoader(
    "data/backend_templates/embeddings/",
    glob="*.txt",
    loader_cls=TextLoader
)
documents = loader.load()

# Créer les embeddings
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Recherche sémantique
query = "Je veux un site moderne pour ma startup tech"
results = vectorstore.similarity_search(query, k=3)
```

### 2. Avec Recherche Sémantique

```python
# Trouver les templates les plus pertinents
def find_best_templates(user_query: str):
    results = vectorstore.similarity_search(user_query, k=3)
    template_ids = [extract_id(doc.page_content) for doc in results]
    return template_ids
```

### 3. Enrichir le Prompt AI

```python
# Ajouter le contexte des templates trouvés au prompt
relevant_docs = vectorstore.similarity_search(user_request, k=2)
context = "\n\n".join([doc.page_content for doc in relevant_docs])

prompt = f"""
Contexte des templates pertinents:
{context}

Requête utilisateur: {user_request}

Recommande les meilleurs templates.
"""
```

## 📊 Contenu de chaque fichier

### Structure type:

```
# Template: [Nom]

**ID:** [id_technique]
**Catégorie:** [Catégorie]
**Layout:** [Type de layout]

## Description
[Description complète et contextualisée]

## Pages incluses
- Liste des pages

## Fonctionnalités
- Liste des features

## Style visuel
[Description détaillée de l'apparence]

## Couleurs
- Primaire: [Code HEX] - [Signification]
- Secondaire: [Code HEX] - [Signification]

## Typographie recommandée
- Titres: [Police]
- Corps: [Police]

## Cas d'usage idéaux
- Liste des scénarios

## Mots-clés
[Liste de mots-clés pour recherche sémantique]
```

## 🎯 Avantages

### ✅ Pour l'AI:

- **Plus de contexte** - Descriptions riches vs JSON brut
- **Compréhension sémantique** - Mots-clés naturels
- **Meilleure matching** - Similarité textuelle
- **Explications** - Pourquoi un template convient

### ✅ Pour le système:

- **Recherche avancée** - Au-delà du matching exact
- **Flexibilité** - Comprend les synonymes
- **Scalabilité** - Facile d'ajouter des templates
- **Documentation** - Fichiers lisibles par humains

## 🔄 Maintenance

### Ajouter un nouveau template:

1. **Créer le JSON** dans `backend_templates/`
2. **Créer le fichier texte** dans `embeddings/` avec:
   - Description complète
   - Tous les champs structurés
   - Mots-clés pertinents
3. **Regénérer les embeddings** (si utilisation vectorielle)

### Template du fichier texte:

```markdown
# Template: [Nom Clair]

**ID:** [id_json]
**Catégorie:** [catégorie]
**Layout:** [type_layout]

## Description

[3-4 phrases descriptives complètes]

## Pages incluses

- [Liste]

## Fonctionnalités

- [Liste des features avec descriptions]

## Style visuel

[Paragraphe sur l'apparence et l'atmosphère]

## Couleurs

- Primaire: [#HEX] - [Signification émotionnelle]
- Secondaire: [#HEX] - [Signification émotionnelle]

## Typographie recommandée

- Titres: [Police] ([style])
- Corps: [Police] ([style])

## Cas d'usage idéaux

- [5-10 cas concrets]

## Mots-clés

[20-30 mots séparés par virgules]
```

## 📈 Cas d'usage avancés

### 1. Recherche hybride (keyword + sémantique)

```python
# Combiner recherche par catégorie ET similarité
category_templates = filter_by_category("education")
semantic_results = vectorstore.similarity_search(
    query,
    filter={"category": "education"}
)
```

### 2. Ranking personnalisé

```python
# Score basé sur similarité + préférences utilisateur
def rank_templates(query, user_preferences):
    results = vectorstore.similarity_search_with_score(query)
    # Ajuster scores selon préférences
    return sorted_results
```

### 3. Explication des choix

```python
# Utiliser le texte pour expliquer pourquoi template recommandé
def explain_choice(template_id):
    doc = load_embedding_file(template_id)
    return extract_key_points(doc.page_content)
```

## 📝 Notes

- **Format texte** - Facilite la lecture par l'AI
- **Richesse sémantique** - Plus d'informations que JSON
- **Maintenance** - Garder synchronisé avec JSON
- **Évolutif** - Facile d'enrichir avec plus de détails

## 🔗 Liens

- JSON sources: `data/backend_templates/*.json`
- Design system: `data/design_system.json`
- Documentation: `data/design_notes/analysis.md`

---

**Date:** 20 février 2026  
**Version:** 1.0  
**Status:** ✅ 11 templates convertis en format texte pour embedding
