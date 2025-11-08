# Estados del Sistema - Estructura y Documentación

## 📁 Estructura de Archivos

La jerarquía de estados ha sido reorganizada de la siguiente manera:

```
BACKEND/
└── Modelos/
    ├── Estado.py              # Clase abstracta base
    └── estados/               # Subcarpeta con estados concretos
        ├── __init__.py
        ├── AutoDetectado.py
        ├── AutoConfirmado.py
        ├── PendienteDeCierre.py
        ├── Derivado.py
        ├── ConfirmadoPorPersonal.py
        ├── Cerrado.py
        ├── Rechazado.py
        ├── BloqueadoEnRevision.py
        ├── PendienteDeRevision.py
        └── SinRevision.py
```

## 🎯 Estados Disponibles

### Estados según el Diagrama de Estados

| Estado | Clase | Descripción |
|--------|-------|-------------|
| Auto-detectado | `AutoDetectado` | Eventos detectados automáticamente |
| Auto-confirmado | `AutoConfirmado` | Eventos confirmados automáticamente |
| Pendiente de Cierre | `PendienteDeCierre` | Esperando cierre |
| Derivado | `Derivado` | Derivado a otra instancia |
| Confirmado por Personal | `ConfirmadoPorPersonal` | Confirmado manualmente |
| Cerrado | `Cerrado` | Estado final cerrado |
| Rechazado | `Rechazado` | Rechazado por analista |
| Bloqueado en Revisión | `BloqueadoEnRevision` | Bloqueado para revisión |
| Pendiente de Revisión | `PendienteDeRevision` | Esperando revisión |
| Sin Revisión | `SinRevision` | Sin revisión, anulado |

## 🔄 Transiciones de Estado

Basado en el diagrama proporcionado:

### Desde AutoDetectado
- ➜ **BloqueadoEnRevision**: `bloquear()`

### Desde AutoConfirmado
- ➜ **PendienteDeCierre**: Automático
- ➜ **Derivado**: `derivar()`

### Desde PendienteDeCierre
- ➜ **Cerrado**: `cerrar()`

### Desde Derivado
- ➜ **ConfirmadoPorPersonal**: `confirmar()`
- ➜ **Rechazado**: `rechazar()`

### Desde ConfirmadoPorPersonal
- ➜ **Cerrado**: `cerrar()`

### Desde BloqueadoEnRevision
- ➜ **ConfirmadoPorPersonal**: `confirmar()`
- ➜ **Rechazado**: `rechazar()`

### Desde PendienteDeRevision
- ➜ **BloqueadoEnRevision**: `bloquear()`
- ➜ **SinRevision**: `anular()`

## 💻 Uso

### Importar la clase abstracta

```python
from BACKEND.Modelos.Estado import Estado
```

### Importar estados concretos

```python
from BACKEND.Modelos.estados import (
    AutoDetectado,
    AutoConfirmado,
    BloqueadoEnRevision,
    # ... otros estados
)
```

### Crear un estado usando el factory method

```python
# Crear estado desde nombre
estado = Estado.from_name("Auto-detectado", "EventoSismico")

# Verificar tipo de estado
if estado.esAutoDetectado():
    print("Es auto-detectado")
```

### Crear directamente una instancia

```python
estado = AutoDetectado("EventoSismico")
nombre = estado.getNombreEstado()  # "Auto-detectado"
```

### Realizar transiciones

```python
from datetime import datetime

# Transición desde AutoDetectado a BloqueadoEnRevision
estado_auto = AutoDetectado("EventoSismico")
cambio = estado_auto.bloquear(evento, datetime.now(), usuario)
```

## 🔍 Métodos de Verificación

Cada estado implementa métodos de verificación:

```python
estado.esAutoDetectado()           # True solo para AutoDetectado
estado.esAutoConfirmado()          # True solo para AutoConfirmado
estado.esPendienteDeCierre()       # True solo para PendienteDeCierre
estado.esDerivado()                # True solo para Derivado
estado.esConfirmadoPorPersonal()   # True solo para ConfirmadoPorPersonal
estado.esCerrado()                 # True solo para Cerrado
estado.esRechazado()               # True solo para Rechazado
estado.esBloqueadoEnRevision()     # True solo para BloqueadoEnRevision
estado.esPendienteDeRevision()     # True solo para PendienteDeRevision
estado.esSinRevision()             # True solo para SinRevision
estado.esAmbitoEventoSismico()     # True si ámbito == "EventoSismico"
```

## 📝 Notas de Implementación

1. **Patrón State**: Los estados implementan el patrón de diseño State, encapsulando el comportamiento específico de cada estado.

2. **Clase Abstracta**: `Estado` es una clase abstracta (ABC) que define la interfaz común para todos los estados.

3. **Factory Method**: El método `from_name()` permite crear estados a partir de strings, útil para deserialización desde base de datos.

4. **Transiciones**: Cada estado solo implementa las transiciones permitidas según el diagrama de estados.

5. **Ámbito**: Los estados tienen un ámbito (ej: "EventoSismico") para distinguir estados de diferentes contextos.

## 🧪 Testing

Para verificar que todos los estados funcionan correctamente:

```bash
python test_estados.py
```

Este script prueba:
- Creación de todos los estados
- Métodos de verificación
- Factory method `from_name()`
- Verificación de ámbito
