#!/usr/bin/env python
import webbrowser
import time
import requests

def check_server_status():
    """Verifier si le serveur Django est accessible"""
    try:
        response = requests.get("http://127.0.0.1:8000/api/sentiment/health/", timeout=5)
        return response.status_code == 200
    except:
        return False

def open_interface():
    """Ouvrir l'interface dans le navigateur"""
    if check_server_status():
        print("Serveur Django accessible")
        print("Ouverture de l'interface d'analyse de sentiment...")
        webbrowser.open("http://127.0.0.1:8000")
        print("Interface disponible sur : http://127.0.0.1:8000")
        return True
    else:
        print("Serveur Django non accessible")
        print("Assurez-vous que le serveur Django est demarre avec:")
        print("   python manage.py runserver")
        return False

if __name__ == "__main__":
    print("Test de l'interface d'analyse de sentiment")
    print("="*50)
    success = open_interface()
    if success:
        print("\nURLs disponibles:")
        print("- Interface principale: http://127.0.0.1:8000")
        print("- Administration Django: http://127.0.0.1:8000/admin")
        print("- API Health Check: http://127.0.0.1:8000/api/sentiment/health/")