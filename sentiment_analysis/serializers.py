from rest_framework import serializers
from .models import SentimentAnalysis

class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = ['id', 'text', 'sentiment', 'confidence', 'created_at']
        read_only_fields = ['id', 'created_at']

class TextInputSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=10000, required=True)
    
    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Text cannot be empty.")
        return value.strip()

class SentimentResponseSerializer(serializers.Serializer):
    text = serializers.CharField()
    sentiment = serializers.CharField()
    confidence = serializers.FloatField()
    details = serializers.DictField(required=False)

class SentenceAnalysisSerializer(serializers.Serializer):
    sentence = serializers.CharField()
    sentiment = serializers.CharField()
    confidence = serializers.FloatField()