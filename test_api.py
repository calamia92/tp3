#!/usr/bin/env python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_endpoint():
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/sentiment/health/")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_sentiment_analysis():
    print("\nTesting sentiment analysis...")
    try:
        data = {"text": "I love this Django application! It's amazing!"}
        response = requests.post(
            f"{BASE_URL}/api/sentiment/analyze/", 
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Sentiment analysis: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Text: {result['text']}")
            print(f"Sentiment: {result['sentiment']}")
            print(f"Confidence: {result['confidence']}")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return False

def test_sentence_analysis():
    print("\nTesting sentence analysis...")
    try:
        data = {"text": "I love programming. However, debugging can be frustrating. But solving problems is rewarding!"}
        response = requests.post(
            f"{BASE_URL}/api/sentiment/analyze-sentences/", 
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Sentence analysis: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Total sentences: {result['total_sentences']}")
            for i, sentence in enumerate(result['sentences'], 1):
                print(f"  {i}. '{sentence['sentence']}' -> {sentence['sentiment']} ({sentence['confidence']:.4f})")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Sentence analysis failed: {e}")
        return False

def test_history():
    print("\nTesting history endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/sentiment/history/")
        print(f"History: {response.status_code}")
        if response.status_code == 200:
            history = response.json()
            print(f"Total analyses in history: {len(history)}")
            if history:
                print(f"Latest analysis: {history[0]['sentiment']} ({history[0]['confidence']})")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"History check failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Django Sentiment Analysis API ===")
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Sentence Analysis", test_sentence_analysis), 
        ("History", test_history)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results.append((test_name, success))
        print(f"{'PASS' if success else 'FAIL'}: {test_name}")
    
    print(f"\n{'='*50}")
    print("SUMMARY:")
    for test_name, success in results:
        print(f"  {test_name}: {'✓' if success else '✗'}")
    
    all_passed = all(success for _, success in results)
    print(f"\nAll tests {'PASSED' if all_passed else 'FAILED'}")