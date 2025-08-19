from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import SentimentAnalysis
from .serializers import (
    SentimentAnalysisSerializer, 
    TextInputSerializer,
    SentimentResponseSerializer,
    SentenceAnalysisSerializer
)
from .services import SentimentAnalysisService
import logging

logger = logging.getLogger(__name__)

sentiment_service = SentimentAnalysisService()

class SentimentAnalysisListView(generics.ListAPIView):
    queryset = SentimentAnalysis.objects.all()
    serializer_class = SentimentAnalysisSerializer

@api_view(['POST'])
def analyze_text_sentiment(request):
    serializer = TextInputSerializer(data=request.data)
    
    if serializer.is_valid():
        text = serializer.validated_data['text']
        
        try:
            result = sentiment_service.analyze_sentiment(text)
            
            sentiment_obj = SentimentAnalysis.objects.create(
                text=text,
                sentiment=result['sentiment'],
                confidence=result['confidence']
            )
            
            response_data = {
                'id': sentiment_obj.id,
                'text': text,
                'sentiment': result['sentiment'],
                'confidence': result['confidence'],
                'details': result.get('details', {}),
                'created_at': sentiment_obj.created_at
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return Response(
                {'error': 'Internal server error occurred during analysis'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def analyze_sentences(request):
    serializer = TextInputSerializer(data=request.data)
    
    if serializer.is_valid():
        text = serializer.validated_data['text']
        
        try:
            results = sentiment_service.analyze_sentences(text)
            
            return Response({
                'original_text': text,
                'sentences': results,
                'total_sentences': len(results)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in sentence analysis: {e}")
            return Response(
                {'error': 'Internal server error occurred during sentence analysis'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def health_check(request):
    try:
        test_result = sentiment_service.analyze_sentiment("This is a test")
        return JsonResponse({
            'status': 'healthy',
            'service': 'sentiment-analysis',
            'model': 'distilbert-base-uncased-finetuned-sst-2-english'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
