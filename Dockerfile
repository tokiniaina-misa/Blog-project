# Utilise une image Python officielle
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /code

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code
COPY . .

# Expose le port utilisé par Django
EXPOSE 8000

# Commande par défaut (surchargée par docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]