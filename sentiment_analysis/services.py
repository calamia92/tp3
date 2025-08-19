from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import logging

logger = logging.getLogger(__name__)

class SentimentAnalysisService:
    def __init__(self):
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=True
            )
            
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt')
                
        except Exception as e:
            logger.error(f"Error initializing sentiment analysis service: {e}")
            raise
    
    def analyze_sentiment(self, text):
        try:
            if not text or not text.strip():
                return {
                    'sentiment': 'neutral',
                    'confidence': 0.5,
                    'details': []
                }
            
            results = self.analyzer(text)
            
            if results and len(results) > 0:
                result = results[0]
                
                positive_score = 0
                negative_score = 0
                
                for score_dict in result:
                    if score_dict['label'] == 'POSITIVE':
                        positive_score = score_dict['score']
                    elif score_dict['label'] == 'NEGATIVE':
                        negative_score = score_dict['score']
                
                if positive_score > negative_score:
                    sentiment = 'positive'
                    confidence = positive_score
                else:
                    sentiment = 'negative' 
                    confidence = negative_score
                
                if abs(positive_score - negative_score) < 0.1:
                    sentiment = 'neutral'
                    confidence = 0.5
                
                return {
                    'sentiment': sentiment,
                    'confidence': round(confidence, 4),
                    'details': {
                        'positive_score': round(positive_score, 4),
                        'negative_score': round(negative_score, 4)
                    }
                }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'sentiment': 'error',
                'confidence': 0.0,
                'details': {'error': str(e)}
            }
    
    def analyze_sentences(self, text):
        try:
            sentences = sent_tokenize(text)
            results = []
            
            for sentence in sentences:
                if sentence.strip():
                    result = self.analyze_sentiment(sentence.strip())
                    results.append({
                        'sentence': sentence.strip(),
                        'sentiment': result['sentiment'],
                        'confidence': result['confidence']
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing sentences: {e}")
            return []