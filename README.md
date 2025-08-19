# Django Sentiment Analysis Web App

Une application web Django avec Django REST Framework qui utilise le modèle DistilBERT de Hugging Face pour l'analyse de sentiments.

## Fonctionnalités

- Analyse de sentiment en temps réel avec DistilBERT
- API REST pour l'analyse de texte
- Analyse par phrases individuelles
- Historique des analyses
- Interface d'administration Django
- Support CORS pour les applications frontend

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Effectuer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Créer un superutilisateur (optionnel) :
```bash
python manage.py createsuperuser
```

4. Lancer le serveur :
```bash
python manage.py runserver
```

## Interface Graphique

L'application propose une **interface web moderne et intuitive** pour analyser les sentiments :

### 🌐 Accès à l'interface :
- **URL principale** : http://127.0.0.1:8000
- **Interface d'administration** : http://127.0.0.1:8000/admin (admin/admin123)

### ✨ Fonctionnalités de l'interface :
1. **Analyse de texte en temps réel** avec DistilBERT
2. **Analyse par phrases** pour des textes longs
3. **Historique des analyses** avec sauvegarde automatique
4. **Exemples de textes** pour tester facilement
5. **Statistiques de confiance** avec barres de progression
6. **Interface responsive** (PC, tablette, mobile)
7. **Raccourcis clavier** (Ctrl+Entrée pour analyser)

### 🎯 Comment utiliser l'interface :
1. Ouvrez http://127.0.0.1:8000 dans votre navigateur
2. Tapez ou collez votre texte dans la zone de saisie
3. Cliquez sur "Analyser le sentiment" ou utilisez Ctrl+Entrée
4. Consultez les résultats avec le score de confiance
5. Explorez l'historique de vos analyses

## Endpoints API

### 1. Analyser un texte
- **URL**: `/api/sentiment/analyze/`
- **Méthode**: `POST`
- **Corps**: `{"text": "Votre texte ici"}`
- **Réponse**: 
```json
{
    "id": 1,
    "text": "Votre texte ici",
    "sentiment": "positive",
    "confidence": 0.9845,
    "details": {
        "positive_score": 0.9845,
        "negative_score": 0.0155
    },
    "created_at": "2023-12-07T10:30:00Z"
}
```

### 2. Analyser par phrases
- **URL**: `/api/sentiment/analyze-sentences/`
- **Méthode**: `POST`
- **Corps**: `{"text": "Première phrase. Deuxième phrase."}`
- **Réponse**:
```json
{
    "original_text": "Première phrase. Deuxième phrase.",
    "sentences": [
        {
            "sentence": "Première phrase.",
            "sentiment": "positive",
            "confidence": 0.8234
        },
        {
            "sentence": "Deuxième phrase.",
            "sentiment": "neutral",
            "confidence": 0.5123
        }
    ],
    "total_sentences": 2
}
```

### 3. Historique des analyses
- **URL**: `/api/sentiment/history/`
- **Méthode**: `GET`
- **Réponse**: Liste de toutes les analyses précédentes

### 4. Vérification de santé
- **URL**: `/api/sentiment/health/`
- **Méthode**: `GET`
- **Réponse**: Status du service

## Modèles utilisés

- **DistilBERT**: `distilbert-base-uncased-finetuned-sst-2-english` pour l'analyse de sentiment
- **NLTK**: Pour la tokenisation des phrases

## Technologies

- Django 4.2.7
- Django REST Framework 3.14.0
- Transformers (Hugging Face) 4.35.2
- PyTorch 2.1.1
- NLTK 3.8.1
- django-cors-headers 4.3.1

## Administration

Accédez à l'interface d'administration Django à `/admin/` pour voir l'historique des analyses.