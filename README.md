# Projet Cloud Native & DevOps 2026

Plateforme événementielle déployée sur Azure Kubernetes Service (AKS) avec une architecture Cloud-Native.

## 🚀 Architecture
- **Backend :** Python Flask (API REST)
- **Base de données :** Azure Blob Storage (Stockage JSON)
- **Conteneurisation :** Docker (Image légère & sécurisée)
- **Orchestration :** Kubernetes (AKS)
- **CI/CD :** GitHub Actions

## 🔧 Installation Locale (Docker)
1. Construire l'image :
   docker build -t projet-cloud .
2. Lancer le conteneur (avec la clé Azure) :
   docker run -p 5000:5000 -e BLOB_CONNECTION_STRING="votre_cle_ici" projet-cloud

## ☁️ Déploiement sur Azure (AKS)
1. Créer le secret Kubernetes :
   kubectl apply -f k8s/secret.yaml
2. Déployer l'application et le service :
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml

## 👤 Auteur
- **Nom :** DAYAWA Germain Mike
- **Projet :** Master 1 Cybersécurité
