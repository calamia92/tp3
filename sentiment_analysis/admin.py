from django.contrib import admin
from .models import SentimentAnalysis

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'sentiment', 'confidence', 'created_at']
    list_filter = ['sentiment', 'created_at']
    search_fields = ['text']
    readonly_fields = ['created_at']
    
    def text_preview(self, obj):
        return obj.text[:100] + "..." if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Text Preview"
