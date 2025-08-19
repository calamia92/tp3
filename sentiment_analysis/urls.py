from django.urls import path
from . import views

app_name = 'sentiment_analysis'

urlpatterns = [
    path('analyze/', views.analyze_text_sentiment, name='analyze_sentiment'),
    path('analyze-sentences/', views.analyze_sentences, name='analyze_sentences'),
    path('history/', views.SentimentAnalysisListView.as_view(), name='sentiment_history'),
    path('health/', views.health_check, name='health_check'),
]