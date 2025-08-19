from django.db import models

class SentimentAnalysis(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.sentiment} ({self.confidence:.2f}) - {self.text[:50]}..."
