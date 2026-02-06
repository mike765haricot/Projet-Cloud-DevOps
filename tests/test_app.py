import pytest
import sys
import os
import time
import json

# --- 1. AJOUT DU DOSSIER APP AU CHEMIN ---
# Cela permet à Python de trouver votre fichier app.py même s'il est dans un autre dossier
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app import app, local_cache

# --- 2. CONFIGURATION DU CLIENT DE TEST ---
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# --- 3. TESTS DE SANTÉ (OBLIGATOIRES) ---

def test_healthz(client):
    """Vérifie que l'application répond 'healthy' (Code 200)"""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json == {"status": "healthy", "service": "flask-api"}

def test_readyz(client):
    """Vérifie la route readyz"""
    response = client.get('/readyz')
    # On accepte 200 ou 503 selon si la clé est là ou pas, car le test doit passer partout
    assert response.status_code in [200, 503]

# --- 4. TESTS FONCTIONNELS (AVEC MOCKING) ---
# Astuce : On remplit le cache local pour ne PAS avoir besoin d'Azure pour le test

def test_get_events_mocked(client):
    """Test de la route /api/events avec des données simulées"""
    # Préparation des fausses données
    fake_events = [{"id": 1, "title": "Test Event"}]
    
    # Injection dans le cache (Mocking manuel)
    local_cache["events.json"] = (fake_events, time.time())
    
    # Appel de l'API
    response = client.get('/api/events')
    
    # Vérifications
    assert response.status_code == 200
    assert response.json == fake_events
    assert response.json[0]['title'] == "Test Event"

def test_get_news_mocked(client):
    """Test de la route /api/news"""
    fake_news = [{"id": 1, "title": "Fake News"}]
    local_cache["news.json"] = (fake_news, time.time())
    
    response = client.get('/api/news')
    assert response.status_code == 200
    assert response.json == fake_news

def test_get_faq_mocked(client):
    """Test de la route /api/faq"""
    fake_faq = [{"question": "Quoi ?", "answer": "Feur"}]
    local_cache["faq.json"] = (fake_faq, time.time())
    
    response = client.get('/api/faq')
    assert response.status_code == 200
    assert response.json == fake_faq