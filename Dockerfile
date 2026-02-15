# 1. On part d'une image Python officielle (légère)
FROM python:3.9-slim

# 2. On crée un dossier de travail dans le conteneur
WORKDIR /app

# 3. On copie le fichier des dépendances (qu'on va créer juste après)
COPY requirements.txt .

# 4. On installe les librairies
RUN pip install --no-cache-dir -r requirements.txt

# 5. On copie tout ton code dans le conteneur
COPY . .

# 6. La commande qui se lance quand on démarre le conteneur
CMD ["python", "main.py"]