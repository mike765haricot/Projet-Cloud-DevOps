# 1. On part d'une image Python officielle très légère ("slim")
# Cela réduit la taille et la surface d'attaque 
FROM python:3.12-slim

# 2. On définit des variables pour éviter que Python n'écrive des fichiers temporaires
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Création d'un utilisateur "non-root" pour la sécurité [cite: 871, 920]
# Si un pirate entre dans le conteneur, il ne sera pas administrateur
RUN useradd -m appuser

# 4. On définit le dossier de travail dans le conteneur
WORKDIR /app

# 5. On copie d'abord les dépendances (pour optimiser le cache Docker)
COPY app/requirements.txt .

# 6. Installation des dépendances sans cache inutile [cite: 872]
RUN pip install --no-cache-dir -r requirements.txt

# 7. On copie le reste du code de l'application
COPY app/ app/

# 8. On change le propriétaire des fichiers pour notre utilisateur sécurisé
RUN chown -R appuser:appuser /app

# 9. On bascule sur l'utilisateur sécurisé (On quitte le mode root)
USER appuser

# 10. On informe Docker que l'app écoute sur le port 5000
EXPOSE 5000

# 11. Commande de démarrage : On utilise Gunicorn (serveur de production)
# bind 0.0.0.0 permet d'être accessible depuis l'extérieur du conteneur
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]