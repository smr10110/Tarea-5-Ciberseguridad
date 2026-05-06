# Tarea 5 — Análisis de Exposición de Secretos

Escaneo de repositorios públicos de HuggingFace con [Gitleaks](https://github.com/gitleaks/gitleaks).

## Requisitos

- Docker Desktop
- VS Code con la extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Pasos para arrancar

### 1. Abrir en el devcontainer

Abre la carpeta del proyecto en VS Code y ejecuta el comando:

```
Dev Containers: Reopen in Container
```

Esto construye la imagen con Python 3.12, uv y gitleaks, y crea el entorno virtual automáticamente en `.venv`.

### 2. Ejecutar el escáner

Desde la terminal integrada del contenedor, corre:

```bash
python scripts/escanear.py
```

El script clona los 10 repositorios más populares de HuggingFace, los escanea con Gitleaks y guarda los resultados en `resultados/all_findings.json`.

### 3. Abrir el notebook

Abre `nbs/tarea5_analisis_secretos.ipynb` y selecciona el kernel **Python (venv)** cuando VS Code lo solicite.

Luego ejecuta todas las celdas con **Run All**.
