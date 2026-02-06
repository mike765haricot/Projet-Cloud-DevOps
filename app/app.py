import os
import json
import time
from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

app = Flask(__name__)

# --- CONFIGURATION ---
# On récupère la clé Azure depuis les variables d'environnement (Sécurité !)
BLOB_CONN_STR = os.getenv("BLOB_CONNECTION_STRING")
CONTAINER_NAME = "content"
CACHE_TTL = 60  # Durée du cache en secondes (demandé dans le sujet)

# Cache en mémoire simple : { "nom_fichier": (donnees, timestamp) }
local_cache = {}

def get_data_from_blob(filename):
    """
    Fonction intelligente qui vérifie d'abord le cache local.
    Si le cache est expiré ou vide, elle va chercher sur Azure.
    """
    current_time = time.time()

    # 1. Vérification du Cache
    if filename in local_cache:
        data, timestamp = local_cache[filename]
        if current_time - timestamp < CACHE_TTL:
            print(f"[CACHE] Lecture locale pour {filename}")
            return data

    # 2. Si pas de cache, on interroge Azure
    if not BLOB_CONN_STR:
        return {"error": "La chaîne de connexion Azure est manquante !"}

    print(f"[AZURE] Téléchargement de {filename} depuis le Blob Storage...")
    try:
        # Connexion au service Azure
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STR)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=filename)
        
        # Téléchargement et lecture
        download_stream = blob_client.download_blob()
        json_data = json.loads(download_stream.readall())

        # Mise à jour du cache
        local_cache[filename] = (json_data, current_time)
        return json_data

    except ResourceNotFoundError:
        return {"error": f"Le fichier {filename} est introuvable sur Azure."}
    except Exception as e:
        return {"error": f"Erreur système : {str(e)}"}

# --- ENDPOINTS API (Demandés dans le sujet) ---

@app.route('/api/events', methods=['GET'])
def get_events():
    # Récupère events.json [cite: 845]
    return jsonify(get_data_from_blob("events.json"))

@app.route('/api/news', methods=['GET'])
def get_news():
    # Récupère news.json [cite: 847]
    return jsonify(get_data_from_blob("news.json"))

@app.route('/api/faq', methods=['GET'])
def get_faq():
    # Récupère faq.json [cite: 849]
    return jsonify(get_data_from_blob("faq.json"))

# --- HEALTH CHECKS (Demandés pour Kubernetes) ---

@app.route('/healthz', methods=['GET'])
def health_check():
    # Vérification de vie simple [cite: 851]
    return jsonify({"status": "healthy", "service": "flask-api"}), 200

@app.route('/readyz', methods=['GET'])
def readiness_check():
    # Vérification de disponibilité [cite: 853]
    # On vérifie si on a bien la clé Azure configurée
    if BLOB_CONN_STR:
        return jsonify({"status": "ready"}), 200
    else:
        return jsonify({"status": "not_ready", "error": "Missing config"}), 503

# --- INTERFACE WEB MINIMALE ---

@app.route('/')
def home():
    # Interface web simple pour visualiser les données [cite: 856]
    return """
    <h1>Plateforme Cloud-Native 2026</h1>
    <p>Bienvenue sur l'API de diffusion de contenu.</p>
    <ul>
        <li><a href="/api/events">Voir les Événements</a></li>
        <li><a href="/api/news">Voir les Actualités</a></li>
        <li><a href="/api/faq">Voir la FAQ</a></li>
    </ul>
    """

if __name__ == '__main__':
    # Démarrage du serveur local
    app.run(host='0.0.0.0', port=5000, debug=True)