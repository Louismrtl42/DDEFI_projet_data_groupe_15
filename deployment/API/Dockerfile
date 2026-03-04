# 1. Image de base légère avec Python 3.9
FROM python:3.9-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier des dépendances (situé à la racine du projet)
# Note : Lors du build, on s'assure que Docker y a accès
COPY ../../requirements.txt .

# 4. Installer les bibliothèques nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le code de l'API et le modèle (.pkl) dans le conteneur
COPY . .

# 6. Exposer le port utilisé par FastAPI
EXPOSE 8000

# 7. Lancer l'API
# On change l'host en 0.0.0.0 pour que l'API soit accessible hors du conteneur
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]