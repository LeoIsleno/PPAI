PPAI — Instrucciones rápidas para ejecutar (Windows / cmd.exe)
==============================================================

Este archivo contiene pasos rápidos para arrancar el backend, la base de datos y (opcional) el frontend en Windows. No modifica archivos existentes.

1) Abrir cmd.exe y situarse en la raíz del proyecto:

```cmd
cd /d c:\Users\Leo\Desktop\PPAI\PPAI
```

2) Crear y activar un virtualenv (recomendado):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

3) Instalar dependencias:

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si no quieres usar `requirements.txt`:

```cmd
pip install flask flask-cors sqlalchemy
```

4) Inicializar la base de datos (opcional — el backend lo hace automáticamente):

```cmd
python BDD\database.py
```

5) Ejecutar el backend:

```cmd
run-backend.bat
```

o manualmente:

```cmd
python BACKEND\Routes.py
```

6) Servir el frontend (opcional):

```cmd
run-frontend.bat
```

o

```cmd
cd FRONTEND
python -m http.server 8000
```

Notas:
- La DB por defecto es `BDD\sismografos.db` (SQLite). Si quieres usar otra DB, define `DATABASE_URL` antes de arrancar.
- Ejecuta siempre desde la raíz del proyecto para evitar problemas de import.
- Para detener el servidor: Ctrl+C en el terminal donde se ejecuta.

Ubicaciones:
- Backend: `BACKEND/Routes.py`
- DB: `BDD/sismografos.db`
- Frontend: `FRONTEND/` (estático)
- Scripts creados: `run-backend.bat`, `run-frontend.bat`, `requirements.txt`

Si prefieres que añada el contenido de este RUN al `README.md` existente, puedo hacerlo pero **no** lo modificaré sin tu confirmación.   
