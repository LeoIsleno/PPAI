# PPAI - Sistema de Gestión de Eventos Sísmicos# PPAI - Sistema de Gestión de Eventos Sísmicos# PPAI



Sistema de gestión y monitoreo de eventos sísmicos con detección automática, revisión manual y análisis de datos sísmicos.



## 🌟 CaracterísticasSistema de gestión y monitoreo de eventos sísmicos con detección automática, revisión manual y análisis de datos sísmicos.



- **Sistema de Autenticación**: Login seguro con sesión persistente

- **Detección Automática** de eventos sísmicos

- **Revisión Manual** por analistas especializados## Estructura del Proyecto## Getting started

- **Gestión de Estados** con patrón State (10 estados)

- **Registro de Cambios** con trazabilidad completa

- **Control de Usuarios** con roles y permisos

- **Interfaz Moderna**: Diseño responsivo con paleta de colores profesional```To make it easy for you to get started with GitLab, here's a list of recommended next steps.



## 📁 Estructura del ProyectoPPAI/



```├── BACKEND/           # Lógica de negocio y modelos de dominioAlready a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

PPAI/

├── BACKEND/           # Lógica de negocio y modelos de dominio│   ├── Modelos/       # Modelos del dominio

│   ├── Modelos/       # Modelos del dominio

│   │   └── estados/   # Estados concretos del sistema (patrón State)│   │   └── estados/   # Estados concretos del sistema (patrón State)```bash

│   ├── GestorRevisionManual.py

│   ├── ListaEventosSismicos.py│   ├── GestorRevisionManual.py# Clonar el repositorio

│   └── Routes.py

├── BDD/               # Capa de persistencia y base de datos│   ├── ListaEventosSismicos.pygit clone https://labsys.frc.utn.edu.ar/gitlab/melo401860/ppai.git

│   ├── repositories/  # Repositorios para acceso a datos

│   ├── orm_models.py  # Modelos ORM (SQLAlchemy)│   └── Routes.pycd ppai

│   └── database.py    # Configuración de BD

└── FRONTEND/          # Interfaz de usuario├── BDD/               # Capa de persistencia y base de datos

    ├── static/        # JavaScript y CSS

    ├── login.html     # Página de inicio de sesión│   ├── repositories/  # Repositorios para acceso a datos# Instalar dependencias (si tienes requirements.txt)

    ├── index.html     # Dashboard principal

    └── *.html         # Otras páginas│   ├── orm_models.py  # Modelos ORM (SQLAlchemy)pip install -r requirements.txt

```

│   └── database.py    # Configuración de BD

## 🎨 Diseño de Interfaz

└── FRONTEND/          # Interfaz de usuario# Inicializar la base de datos

### Paleta de Colores

- **Azul Profundo** (`#1a237e`): Estabilidad y confiabilidad    ├── static/        # JavaScriptpython -c "from BDD.database import init_db; init_db()"

- **Azul Índigo** (`#283593`): Color principal del sistema

- **Verde Azulado** (`#00897b`): Monitoreo activo    └── *.html         # Páginas HTML```

- **Naranja** (`#f57c00`): Alertas y advertencias

- **Rojo** (`#c62828`): Eventos críticos```

- **Verde** (`#2e7d32`): Confirmaciones

## Uso

Ver documentación completa de diseño en [`FRONTEND/DESIGN.md`](FRONTEND/DESIGN.md)

## Características Principales

## 🔐 Estados del Sistema

### Iniciar el Backend

El sistema implementa 10 estados para el ciclo de vida de eventos sísmicos:

- **Detección Automática** de eventos sísmicos

1. **Auto-detectado** - Evento detectado automáticamente

2. **Auto-confirmado** - Evento confirmado automáticamente- **Revisión Manual** por analistas especializados```bash

3. **Pendiente de Cierre** - Esperando cierre

4. **Derivado** - Derivado a otra instancia- **Gestión de Estados** con patrón State (10 estados)cd BACKEND

5. **Confirmado por Personal** - Confirmado manualmente

6. **Cerrado** - Estado final cerrado- **Registro de Cambios** con trazabilidad completapython Routes.py

7. **Rechazado** - Rechazado por analista

8. **Bloqueado en Revisión** - Bloqueado para revisión- **Control de Usuarios** con roles y permisos```

9. **Pendiente de Revisión** - Esperando revisión

10. **Sin Revisión** - Sin revisión, anulado



> Ver documentación completa en `BACKEND/Modelos/estados/README.md`## Estados del Sistema### Acceder a la Interfaz Web



## ⚙️ Requisitos



- Python 3.8+El sistema implementa 10 estados para el ciclo de vida de eventos sísmicos:Abrir en el navegador: `http://localhost:5000`

- SQLAlchemy

- Flask (para el backend API)



## 🚀 Instalación1. **Auto-detectado** - Evento detectado automáticamente## Arquitectura



```bash2. **Auto-confirmado** - Evento confirmado automáticamente

# Clonar el repositorio

git clone https://labsys.frc.utn.edu.ar/gitlab/melo401860/ppai.git3. **Pendiente de Cierre** - Esperando cierre### Patrón de Diseño: State

cd ppai

4. **Derivado** - Derivado a otra instancia

# Instalar dependencias (si tienes requirements.txt)

pip install -r requirements.txt5. **Confirmado por Personal** - Confirmado manualmenteEl sistema utiliza el patrón State para gestionar el ciclo de vida de los eventos sísmicos. Cada estado concreto implementa su propia lógica de transición.



# Inicializar la base de datos6. **Cerrado** - Estado final cerrado

python -c "from BDD.database import init_db; init_db()"

```7. **Rechazado** - Rechazado por analista**Ejemplo de uso:**



## 💻 Uso8. **Bloqueado en Revisión** - Bloqueado para revisión



### Iniciar el Backend9. **Pendiente de Revisión** - Esperando revisión```python



```bash10. **Sin Revisión** - Sin revisión, anuladofrom BACKEND.Modelos.Estado import Estado

cd BACKEND

python Routes.pyfrom BACKEND.Modelos.estados import AutoDetectado, BloqueadoEnRevision

```

> Ver documentación completa en `BACKEND/Modelos/estados/README.md`

El servidor se iniciará en `http://localhost:5001`

# Crear estado

### Acceder a la Interfaz Web

## Requisitosestado = AutoDetectado("EventoSismico")

1. Abrir en el navegador: `http://localhost:5001`

2. Iniciar sesión con las credenciales de prueba:



**Credenciales disponibles:**- Python 3.8+# Realizar transición

- **Usuario**: `nico` / **Contraseña**: `123`

- **Usuario**: `admin` / **Contraseña**: `admin123`- SQLAlchemynuevo_cambio = evento.bloquear(estado_bloqueado, fecha_actual, usuario)

- **Usuario**: `analista` / **Contraseña**: `analista123`

- Flask (para el backend API)```

### Navegación del Sistema



```

Login (/)## Instalación### Base de Datos

  └─> Panel de Control (index.html)

       ├─> Registrar Revisión Manual (registrar.html)

       │    └─> Datos del Evento (datos_evento.html)

       ├─> Visualizar Estadísticas```bash- **ORM:** SQLAlchemy

       ├─> Gestionar Alertas

       └─> Configuración del Sistema# Clonar el repositorio- **Base de datos:** SQLite (por defecto)

```

git clone https://labsys.frc.utn.edu.ar/gitlab/melo401860/ppai.git- **Tablas principales:** 

## 🏗️ Arquitectura

cd ppai  - `evento_sismico` - Eventos sísmicos

### Patrón de Diseño: State

  - `estado` - Estados del sistema

El sistema utiliza el patrón State para gestionar el ciclo de vida de los eventos sísmicos. Cada estado concreto implementa su propia lógica de transición.

# Instalar dependencias (si tienes requirements.txt)  - `cambio_estado` - Historial de cambios

**Ejemplo de uso:**

pip install -r requirements.txt  - `usuario` - Usuarios del sistema

```python

from BACKEND.Modelos.Estado import Estado

from BACKEND.Modelos.estados import AutoDetectado, BloqueadoEnRevision

# Inicializar la base de datos## Documentación Adicional

# Crear estado

estado = AutoDetectado("EventoSismico")python -c "from BDD.database import init_db; init_db()"



# Realizar transición```- **Estados:** `BACKEND/Modelos/estados/README.md` - Documentación completa de estados

nuevo_cambio = evento.bloquear(estado_bloqueado, fecha_actual, usuario)

```- **Transiciones:** `BACKEND/Modelos/estados/TRANSICIONES.md` - Diagrama de transiciones



### Patrón Repository## Uso



Separación entre lógica de negocio y persistencia de datos:## Autores



```python### Iniciar el Backend

from BDD.repositories.evento_repository import EventoRepository

from BDD.database import SessionLocalProyecto PPAI - UTN FRC



db = SessionLocal()```bash

evento_orm = EventoRepository.from_domain(db, evento_dominio)

db.commit()cd BACKEND## Licencia

```

python Routes.py

### Base de Datos

```Proyecto académico - UTN Facultad Regional Córdoba

- **ORM:** SQLAlchemy

- **Base de datos:** SQLite (por defecto, configurable)

- **Tablas principales:** ### Acceder a la Interfaz Web

  - `evento_sismico` - Eventos sísmicos

  - `estado` - Estados del sistemaAbrir en el navegador: `http://localhost:5000`

  - `cambio_estado` - Historial de cambios

  - `usuario` - Usuarios del sistema## Arquitectura

  - `empleado` - Datos de empleados

  - `rol` - Roles del sistema### Patrón de Diseño: State



## 📚 Documentación AdicionalEl sistema utiliza el patrón State para gestionar el ciclo de vida de los eventos sísmicos. Cada estado concreto implementa su propia lógica de transición.



- **Estados**: `BACKEND/Modelos/estados/README.md` - Documentación completa de estados**Ejemplo de uso:**

- **Transiciones**: `BACKEND/Modelos/estados/TRANSICIONES.md` - Diagrama de transiciones

- **Diseño UI**: `FRONTEND/DESIGN.md` - Guía de diseño de interfaz```python

from BACKEND.Modelos.Estado import Estado

## 🔒 Seguridadfrom BACKEND.Modelos.estados import AutoDetectado, BloqueadoEnRevision



- Autenticación requerida para todas las páginas (excepto login)# Crear estado

- Sesión con timeout de 24 horasestado = AutoDetectado("EventoSismico")

- Opción de "Recordar sesión"

- Validación de credenciales# Realizar transición

- Protección de rutas en el frontendnuevo_cambio = evento.bloquear(estado_bloqueado, fecha_actual, usuario)

```

## 👥 Autores

### Base de Datos

Proyecto PPAI - UTN FRC

- **ORM:** SQLAlchemy

## 📄 Licencia- **Base de datos:** SQLite (por defecto)

- **Tablas principales:** 

Proyecto académico - UTN Facultad Regional Córdoba  - `evento_sismico` - Eventos sísmicos

  - `estado` - Estados del sistema

---  - `cambio_estado` - Historial de cambios

  - `usuario` - Usuarios del sistema

**Última actualización**: Noviembre 2025

## Documentación Adicional

- **Estados:** `BACKEND/Modelos/estados/README.md` - Documentación completa de estados
- **Transiciones:** `BACKEND/Modelos/estados/TRANSICIONES.md` - Diagrama de transiciones

## Autores

Proyecto PPAI - UTN FRC

## Licencia

Proyecto académico - UTN Facultad Regional Córdoba
