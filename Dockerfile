FROM python:3.14-slim

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copier les fichiers de dépendances
COPY pyproject.toml .
COPY .python-version .

# Installer les dépendances
RUN uv sync

# Copier le reste du code
COPY static/ ./static/
COPY templates/ ./templates/
COPY app.py .

# Exposer un port (optionnel, utile pour Flask/FastAPI)
EXPOSE 5050

# Commande par défaut
CMD ["uv", "run", "app.py"]
